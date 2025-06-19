from pyrogram import Client, filters, types
from pyrogram.enums import ChatMemberStatus
from collections import deque
import asyncio
import time

# Track spam messages and mute status
spam_tracker = {}     # {chat_id: {user_id: deque}}
muted_users = {}      # {user_id: mute_expiry}
tracker_lock = asyncio.Lock()

# Settings
SPAM_LIMIT = 5         # max messages
TIME_WINDOW = 7        # seconds
MUTE_DURATION = 300    # 5 minutes

# ✅ Mute spammers in group & bot
@Client.on_message(filters.group & ~filters.service & ~filters.edited)
async def anti_spam_handler(client, message):
    if not message.from_user or message.from_user.is_bot:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id
    now = time.time()

    # ⏳ Remove expired mute
    if user_id in muted_users and muted_users[user_id] <= now:
        del muted_users[user_id]

    # ❌ If already muted, ignore message & don't count for spawn
    if muted_users.get(user_id, 0) > now:
        return

    async with tracker_lock:
        if chat_id not in spam_tracker:
            spam_tracker[chat_id] = {}

        if user_id not in spam_tracker[chat_id]:
            spam_tracker[chat_id][user_id] = deque(maxlen=SPAM_LIMIT + 2)

        spam_tracker[chat_id][user_id].append(now)

        # Count recent messages
        timestamps = spam_tracker[chat_id][user_id]
        recent_msgs = sum(1 for t in timestamps if now - t <= TIME_WINDOW)

        if recent_msgs < SPAM_LIMIT:
            return

        # 🚫 Mute from bot + group
        muted_users[user_id] = now + MUTE_DURATION
        spam_tracker[chat_id][user_id].clear()

    # 🔇 Mute user in group (no admin bypass)
    try:
        await client.restrict_chat_member(
            chat_id,
            user_id,
            permissions=types.ChatPermissions(),  # fully muted
            until_date=int(now + MUTE_DURATION)
        )
        await message.reply(
            f"🚫 {message.from_user.mention} has been muted for 5 minutes for spamming."
        )
        print(f"[AntiSpam] User {user_id} muted in chat {chat_id} + bot blocked.")
    except Exception as e:
        print(f"[AntiSpam] Failed to mute user {user_id} in chat {chat_id}: {e}")

