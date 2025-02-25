# YxH/Plugins/clean.py
from pyrogram import Client, filters
from ..Database.users import get_all_users
from config import OWNER_ID

@Client.on_message(filters.command("permaclean") & filters.user(OWNER_ID))
async def permanent_clean(_, m):
    users = await get_all_users()
    for user in users:
        await user.update()  # Force re-save with new structure
    await m.reply(f"♻️ Permanently cleaned {len(users)} users!")
