from pyrogram import filters
from pyrogram.types import ChatPermissions, Message
from datetime import datetime, timedelta
import asyncio
import time
from ..universal_decorator import YxH


spam_tracker: dict[tuple[int, int], list[float]] = {}

SPAM_LIMIT = 5
TIME_WINDOW = 5
MUTE_DURATION = 60

@Clinet.on_message(filters.group & filters.text)
async def anti_spam_mute(client, message: Message):
    try:
        user = message.from_user
        chat_id = message.chat.id
        user_id = user.id
        now = time.time()

        member = await client.get_chat_member(chat_id, user_id)
        if member.status in ("administrator", "creator"):
            return

        key = (chat_id, user_id)
        spam_tracker.setdefault(key, []).append(now)
        spam_tracker[key] = [t for t in spam_tracker[key] if now - t < TIME_WINDOW]

        if len(spam_tracker[key]) > SPAM_LIMIT:
            await client.restrict_chat_member(
                chat_id,
                user_id,
                permissions=ChatPermissions(),
                until_date=datetime.utcnow() + timedelta(seconds=MUTE_DURATION)
            )

            await message.reply_text(f"🚫 {user.mention} muted for spamming.")

            spam_tracker[key] = []
            asyncio.create_task(auto_unmute(client, chat_id, user_id, user.mention))

    except Exception as e:
        print("[AntiSpamError]", e)

async def auto_unmute(client, chat_id, user_id, mention):
    await asyncio.sleep(MUTE_DURATION)
    try:
        await client.restrict_chat_member(
            chat_id,
            user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await client.send_message(chat_id, f"🔈 {mention} has been unmuted.")
    except Exception as e:
        print("[AutoUnmuteError]", e)