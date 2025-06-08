from pyrogram import Client, filters
from ..Database.users import get_user
import time

def format_duration(seconds: int):
    mins = seconds // 60
    hrs, mins = divmod(mins, 60)
    days, hrs = divmod(hrs, 24)
    if days: return f"{days}d {hrs}h {mins}m"
    elif hrs: return f"{hrs}h {mins}m"
    else: return f"{mins}m"

@Client.on_message(filters.command("afk") & filters.group)
async def afk_command(client, message):
    user = await get_user(message.from_user.id)
    reason = " ".join(message.command[1:]) or "AFK"
    user.set_afk(reason)
    await user.update()
    await message.reply(
        f"🌙 {message.from_user.mention} is now AFK!\n"
        f"📌 Reason: `{reason}`"
    )

@Client.on_message(filters.group & filters.text)
async def remove_afk_on_message(client, message):
    if not message.from_user:
        return
    user = await get_user(message.from_user.id)
    if user.is_afk():
        afk_reason = user.get_afk()
        afk_since = user.get_afk_time()
        duration = format_duration(int(time.time() - afk_since))
        user.remove_afk()
        await user.update()

        await message.reply(
            f"☀️ Welcome back {message.from_user.mention}!\n"
            f"You were AFK for `{duration}` (Reason: {afk_reason})."
        )

@Client.on_message(filters.group & filters.reply)
async def notify_afk_on_mention(client, message):
    replied_user = message.reply_to_message.from_user
    if not replied_user:
        return
    user = await get_user(replied_user.id)
    if user.is_afk():
        reason = user.get_afk()
        since = format_duration(int(time.time() - user.get_afk_time()))
        await message.reply(
            f"📣 {replied_user.first_name} is AFK!\n"
            f"📌 Reason: `{reason}`\n"
            f"⏱️ Since: {since} ago"
        )