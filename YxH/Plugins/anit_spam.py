from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, Message
from . import YxH  # your main bot client
import time

# In-memory tracker for user messages
spam_tracker: dict[int, list[float]] = {}

# Anti-spam settings
SPAM_LIMIT = 5        # Messages allowed
TIME_WINDOW = 5       # Seconds window
MUTE_DURATION = 60    # Mute duration in seconds

# Combined filter to avoid syntax error with ~filters.service
filter_spam = (filters.group & filters.text) & ~filters.service

@Client.on_message(filter_spam)
async def anti_spam_mute(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    now = time.time()

    # ✅ Skip if user is admin
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in ("administrator", "creator"):
            return
    except:
        return

    # Store timestamps of recent messages
    spam_tracker.setdefault(user_id, []).append(now)
    spam_tracker[user_id] = [
        ts for ts in spam_tracker[user_id] if now - ts < TIME_WINDOW
    ]

    # Check if user exceeded the limit
    if len(spam_tracker[user_id]) > SPAM_LIMIT:
        try:
            await client.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(),  # No permissions = mute
                until_date=int(now + MUTE_DURATION)
            )

            await message.reply_text(
                f"🚫 {message.from_user.mention} has been muted for spamming "
                f"({MUTE_DURATION} seconds)."
            )

            # Clear the user's history after mute
            spam_tracker[user_id] = []

        except Exception as e:
            await message.reply_text(f"❌ Failed to mute: {e}")