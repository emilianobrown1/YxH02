from pyrogram import Client, filters
from . import YxH, get_anime_character

@Client.on_message(filters.command("xfav"))
@YxH()
async def xf(_, m, u):
    try:
        id = int(m.text.split()[1])
    except:
        return await m.reply("Usage: /xfav [character_id]\n\nTo remove favourite character, `/xfav 0`.")
    if id == 0:
        if not u.favourite_character:
            return await m.reply("There is no favourite character to remove.")
        u.favourite_character = None
        await u.update()
        return await m.reply("Favourite character has been removed.")
    if id == u.favourite_character:
        return await m.reply("No changes, as your previous favourite character was same.")
    char = await get_anime_character(id)
    if not char:
        return await m.reply("Invalid character ID.")
    u.favourite_character = id
    await u.update()
    await m.reply(f"Favourite character has been set to `{char.name} ({char.id})`.")
