from config import SUDO_USERS
from pyrogram import Client, filters

async def get_user(_, m):
    if m.reply_to_message:
        return m.reply_to_message.from_user.id
    try:
        return int(m.text.split()[1])
    except:
        await m.reply("Either reply to an user or provide ID.")
