from config import SUDO_USERS
from pyrogram import Client, filters
from ..Database.users import get_user
from ..Database.characters import get_anime_character

@Client.on_message(filters.command("gold") & filters.user(SUDO_USERS))
async def gold(_, m):
    spl = m.text.split()
    try:
        if m.reply_to_message:
            id, amount = m.reply_to_message.from_user.id, int(spl[1])
        else:
            id, amount = int(spl[1]), int(spl[2])
    except:
        return await m.reply("Usage:\n\n`/gold <id> <amount>`\n`/gold <amount> (Reply to an user)`")
    u = await get_user(id)
    u.gold += amount
    await m.reply(f"Added `{amount}`")
    await u.update()
    
@Client.on_message(filters.command("gems") & filters.user(SUDO_USERS))
async def gems(_, m):
    spl = m.text.split()
    try:
        if m.reply_to_message:
            id, amount = m.reply_to_message.from_user.id, int(spl[1])
        else:
            id, amount = int(spl[1]), int(spl[2])
    except Exception as e:
        await m.reply(e)
        return await m.reply("Usage:\n\n/gems <id> <amount>\n/gems <amount> (Reply to an user)")
    u = await get_user(id)
    u.gems += amount
    await m.reply(f"Added `{amount}`")
    await u.update()
    
@Client.on_message(filters.command("crystals") & filters.user(SUDO_USERS))
async def crystals(_, m):
    spl = m.text.split()
    try:
        if m.reply_to_message:
            id, amount = m.reply_to_message.from_user.id, int(spl[1])
        else:
            id, amount = int(spl[1]), int(spl[2])   
    except:
        return await m.reply("Usage:\n\n/crystals <id> <amount>\n/crystals <amount> (Reply to an user)")
    u = await get_user(id)
    u.crystals += amount
    await m.reply(f"Added `{amount}`")
    await u.update()

@Client.on_message(filters.command("addchar") & filters.user(SUDO_USERS))
async def add_character(_, m):
    spl = m.text.split()
    try:
        if m.reply_to_message:
            user_id, char_id = m.reply_to_message.from_user.id, int(spl[1])
        else:
            user_id, char_id = int(spl[1]), int(spl[2])
    except:
        return await m.reply("Usage:\n\n`/addchar <user_id> <character_id>`\n`/addchar <character_id> (Reply to a user)`")

    user = await get_user(user_id)
    if not user:
        return await m.reply("User not found.")

    character = await get_anime_character(char_id)
    if not character:
        return await m.reply("Character not found.")

    if char_id in user.collection:
        return await m.reply("Character already in user's collection.")

    user.collection.append(char_id)
    await user.update()
    await m.reply(f"Added character `{character.name}` (ID: `{char_id}`) to `{user.username}`'s collection.")
