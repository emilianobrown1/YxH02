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

@Client.on_message(filters.command("addch") & filters.user(SUDO_USERS))
async def addch(_, m):
    spl = m.text.split()
    try:
        if m.reply_to_message:
            id, character_id = m.reply_to_message.from_user.id, int(spl[1])
        else:
            id, character_id = int(spl[1]), int(spl[2])
    except:
        return await m.reply("Usage:\n\n/addch <id> <character_id>\n/addch <character_id> (Reply to an user)")
    
    u = await get_user(id)
    character = await get_anime_character(character_id)
    
    if character:
        # Add the character to the user's collection
        if character_id not in u.collection:
            u.collection[character_id] = character
            await u.update()  # Save the updated user
            await m.reply(f"Character `{character_id}` added to user `{id}`'s collection!")
        else:
            await m.reply(f"User `{id}` already has character `{character_id}` in their collection.")
    else:
        await m.reply("Character not found.")