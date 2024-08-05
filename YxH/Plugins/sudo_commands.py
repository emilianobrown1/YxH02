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


@Client.on_message(filters.command("addcharacter") & filters.user(SUDO_USERS))
async def add_character(_, m):
    spl = m.text.split()
    try:
        if m.reply_to_message:
            user_id = m.reply_to_message.from_user.id
            character_id = int(spl[1])
        else:
            user_id, character_id = int(spl[1]), int(spl[2])
    except:
        return await m.reply("Usage:\n\n`/addcharacter <user_id> <character_id>`\n`/addcharacter <character_id> (Reply to a user)`")
    
    u = await get_user(user_id)
    character = await get_anime_character(character_id)
    
    if not character:
        return await m.reply(f"Character with ID {character_id} not found.")
    
    if character_id in u.collection:
        return await m.reply(f"User already has character {character.name} (ID: {character_id}) in their collection.")
    
    u.collection.append(character_id)
    await u.update()
    
    await m.reply(f"Added character {character.name} (ID: {character_id}) to {u.name}'s collection.")