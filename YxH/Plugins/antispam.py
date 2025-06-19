from pyrogram import Client, filters, types
from collections import deque
import asyncio
import time

# Global anti-spam tracker with locks
spam_tracker = {}
tracker_lock = asyncio.Lock()

# Configuration (adjust as needed)
SPAM_LIMIT = 5         # Max messages allowed in TIME_WINDOW
TIME_WINDOW = 7        # Seconds to monitor for spam
MUTE_DURATION = 300    # 5 minutes (in seconds)
ADMIN_BYPASS = True    # Exempt admins from being muted?

@Client.on_message(filters.group & ~filters.service & ~filters.edited)
async def anti_spam_handler(client, message):
    if not message.from_user or message.from_user.is_bot:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id
    current_time = time.time()

    # Use lock for safe access to spam tracker
    async with tracker_lock:
        if chat_id not in spam_tracker:
            spam_tracker[chat_id] = {}

        if user_id not in spam_tracker[chat_id]:
            spam_tracker[chat_id][user_id] = deque(maxlen=SPAM_LIMIT + 2)

        timestamps = spam_tracker[chat_id][user_id]
        timestamps.append(current_time)

    # Check for spam outside lock for better performance
    if len(timestamps) < SPAM_LIMIT:
        return

    recent_messages = sum(1 for ts in reversed(timestamps) if current_time - ts <= TIME_WINDOW)

    if recent_messages < SPAM_LIMIT:
        return

    # Bypass if admin and ADMIN_BYPASS is True
    if ADMIN_BYPASS:
        try:
            member = await client.get_chat_member(chat_id, user_id)
            if member.status in ("administrator", "creator"):
                return
        except:
            pass

    # Apply mute
    try:
        await client.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=types.ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False
            ),
            until_date=int(current_time + MUTE_DURATION)
        )

        await message.reply(
            f"🚫 {message.from_user.mention} has been muted for {MUTE_DURATION // 60} minutes due to spamming!"
        )

        # Reset tracker for the user after muting
        async with tracker_lock:
            spam_tracker[chat_id][user_id] = deque(maxlen=SPAM_LIMIT + 2)

        print(f"[AntiSpam] Muted user {user_id} in chat {chat_id} for spamming.")

    except Exception as e:
        print(f"[AntiSpam] Failed to mute user {user_id} in chat {chat_id}: {str(e)}")