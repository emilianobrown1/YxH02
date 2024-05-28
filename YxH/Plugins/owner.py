from config import SUDO_USERS
from pyrogram import Client, filters
from ..Database.users import get_user

@Client.on_message(filters.command("gold") & filters.user(SUDO_USERS))
async def gold(_, m):
    spl = m.text.split()
    try:
        id, amount = m.reply_to_message.from_user.id, int(spl[1]) if m.reply_to_message else int(spl[1]), int(spl[2])
    except:
        return await m.reply("Usage:\n\n/gold <id> <amount>\n/gold <amount> (Reply to an user)")
    u = await get_user(id)
    u.gold += amount
    await m.reply(f"Added `{amount}`")
    await u.update()
    
@Client.on_message(filters.command("gems") & filters.user(SUDO_USERS))
async def gems(_, m):
    spl = m.text.split()
    try:
        id, amount = m.reply_to_message.from_user.id, int(spl[1]) if m.reply_to_message else int(spl[1]), int(spl[2])
    except:
        return await m.reply("Usage:\n\n/gems <id> <amount>\n/gems <amount> (Reply to an user)")
    u = await get_user(id)
    u.gems += amount
    await m.reply(f"Added `{amount}`")
    await u.update()
    
@Client.on_message(filters.command("crystals") & filters.user(SUDO_USERS))
async def crystals(_, m):
    spl = m.text.split()
    try:
        id, amount = m.reply_to_message.from_user.id, int(spl[1]) if m.reply_to_message else int(spl[1]), int(spl[2])
    except:
        return await m.reply("Usage:\n\n/crystals <id> <amount>\n/crystals <amount> (Reply to an user)")
    u = await get_user(id)
    u.crystals += amount
    await m.reply(f"Added `{amount}`")