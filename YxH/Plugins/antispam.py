from pyrogram import Client, filters, types
from pyrogram.enums import ChatMemberStatus, ChatType
from collections import defaultdict, deque
import asyncio
import time
from typing import Dict, Deque

# Use defaultdict for cleaner initialization
spam_tracker: Dict[int, Dict[int, Deque[float]] = defaultdict(lambda: defaultdict(lambda: deque(maxlen=SPAM_LIMIT + 2)))
muted_users: Dict[int, float] = {}
tracker_lock = asyncio.Lock()

# Settings
SPAM_LIMIT = 5
TIME_WINDOW = 7
MUTE_DURATION = 300

@Client.on_message(filters.group & ~filters.service & ~filters.edited)
async def anti_spam_handler(client: Client, message: types.Message):
    # Early exit conditions
    if not message.from_user or message.from_user.is_bot:
        return
        
    if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        return

    user_id = message.from_user.id
    chat_id = message.chat.id
    now = time.time()

    # Check if user is admin (shouldn't be muted)
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            return
    except Exception as e:
        print(f"Failed to check user status: {e}")
        return

    # Cleanup expired mutes
    if user_id in muted_users and muted_users[user_id] <= now:
        del muted_users[user_id]

    if muted_users.get(user_id, 0) > now:
        try:
            await message.delete()
        except:
            pass
        return

    async with tracker_lock:
        timestamps = spam_tracker[chat_id][user_id]
        timestamps.append(now)
        recent_msgs = sum(1 for t in timestamps if now - t <= TIME_WINDOW)

        if recent_msgs >= SPAM_LIMIT:
            muted_users[user_id] = now + MUTE_DURATION
            timestamps.clear()
        else:
            return

    # Verify bot has admin permissions
    try:
        bot_member = await client.get_chat_member(chat_id, "me")
        if not bot_member.privileges.can_restrict_members:
            print(f"Bot lacks mute permissions in chat {chat_id}")
            return
    except Exception as e:
        print(f"Failed to check bot permissions: {e}")
        return

    # Perform mute
    try:
        await client.restrict_chat_member(
            chat_id,
            user_id,
            permissions=types.ChatPermissions(),
            until_date=int(now + MUTE_DURATION)
            
        await message.reply(
            f"🚫 {message.from_user.mention} has been muted for {MUTE_DURATION//60} minutes for spamming."
        )
        print(f"Muted user {user_id} in chat {chat_id}")
        
        # Delete spam messages
        async for msg in client.search_messages(chat_id, from_user=user_id, limit=SPAM_LIMIT):
            if now - msg.date.timestamp() <= TIME_WINDOW:
                try:
                    await msg.delete()
                except:
                    continue
                    
    except Exception as e:
        print(f"Failed to mute user {user_id}: {e}")