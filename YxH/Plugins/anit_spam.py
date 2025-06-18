from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, Message
from . import YxH  
import time

# Track messages per user in memory
spam_tracker: dict[int, list[float]] = {}

# Anti-spam configuration
SPAM_LIMIT = 3         # Max messages allowed
TIME_WINDOW = 5       # In seconds
MUTE_DURATION = 60     # Mute time in seconds

@Client.on_message(filters.group & filters.text & ~filters.service)
async def anti_spam_mute(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    now = time.time()

    # ✅ OPTIONAL: skip admins
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in ("administrator", "creator"):
            return  # Don't mute admins
    except:
        return  # If failed to get member, skip

    # Initialize or update message timestamps
    spam_tracker.setdefault(user_id, []).append(now)

    # Keep only recent messages in the defined time window
    spam_tracker[user_id] = [
        ts for ts in spam_tracker[user_id] if now - ts < TIME_WINDOW
    ]

    # If message count exceeds the spam limit
    if len(spam_tracker[user_id]) > SPAM_LIMIT:
        try:
            # Restrict all permissions (mute)
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

            # Clear history after muting
            spam_tracker[user_id] = []

        except Exception as e:
            await message.reply_text(f"❌ Failed to mute: {e}")