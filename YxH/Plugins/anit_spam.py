from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, Message
from datetime import datetime, timedelta
import asyncio
import time
from ..universal_decorator import YxH

spam_tracker: dict[int, list[float]] = {}

SPAM_LIMIT = 5
TIME_WINDOW = 5
MUTE_DURATION = 60  # seconds

filter_spam = filters.group & filters.text & ~filters.service

async def auto_unmute(client, chat_id, user_id, mention):
    await asyncio.sleep(MUTE_DURATION)
    try:
        await client.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await client.send_message(chat_id, f"🔈 {mention} has been automatically unmuted.")
    except Exception as e:
        await client.send_message(chat_id, f"❌ Auto-unmute failed: {e}")

@YxH.on_message(filter_spam)
async def anti_spam_mute(client: Client, message: Message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        now = time.time()

        # Skip admins
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in ("administrator", "creator"):
            return

        # Track user messages
        spam_tracker.setdefault(user_id, []).append(now)
        spam_tracker[user_id] = [ts for ts in spam_tracker[user_id] if now - ts < TIME_WINDOW]

        if len(spam_tracker[user_id]) > SPAM_LIMIT:
            mute_until = datetime.utcnow() + timedelta(seconds=MUTE_DURATION)

            await client.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(),
                until_date=mute_until
            )

            await message.reply_text(
                f"🚫 {message.from_user.mention} has been muted for spamming ({MUTE_DURATION} seconds)."
            )

            spam_tracker[user_id] = []

            # Run auto-unmute in background
            asyncio.create_task(auto_unmute(client, chat_id, user_id, message.from_user.mention))

    except Exception as e:
        await message.reply_text(f"❌ Anti-spam error: {e}")