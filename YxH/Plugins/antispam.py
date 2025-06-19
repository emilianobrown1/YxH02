from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
import time

# Tracks user message timestamps: {chat_id: {user_id: [timestamps]}}
message_tracker = {}

# Configuration
SPAM_LIMIT = 3         # Max messages allowed
SPAM_INTERVAL = 5      # In seconds
MUTE_DURATION = 300    # In seconds (5 minutes)

@Client.on_message(filters.text & filters.private)
async def anti_spam_handler(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Skip bots
    if message.from_user.is_bot:
        return

    now = time.time()
    chat_users = message_tracker.setdefault(chat_id, {})
    user_times = chat_users.setdefault(user_id, [])

    # Remove timestamps older than SPAM_INTERVAL
    user_times = [t for t in user_times if now - t <= SPAM_INTERVAL]
    user_times.append(now)
    chat_users[user_id] = user_times

    # Mute if user exceeded spam limit
    if len(user_times) > SPAM_LIMIT:
        try:
            await client.restrict_chat_member(
                chat_id,
                user_id,
                permissions=ChatPermissions(),  # no permissions = mute
                until_date=int(now + MUTE_DURATION)
            )
            await message.reply(
                f"🚫 [User](tg://user?id={user_id}) has been muted for spamming!",
                disable_web_page_preview=True
            )
        except Exception as e:
            print(f"Failed to mute user {user_id} in chat {chat_id}:", e)

        # Reset tracker to avoid repeat mutes
        chat_users[user_id] = []