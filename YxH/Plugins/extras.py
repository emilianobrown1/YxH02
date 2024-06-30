from pyrogram import Client, filters
from . import YxH, get_anime_character

@Client.on_message(filters.command('extras'))
@YxH()
async def find_duplicates(_, m, u):
    coll_dict: dict = u.collection
    if not coll_dict:
        return await m.reply('Your collection is empty.')
    
    # Find duplicates
    duplicates = {k: v for k, v in coll_dict.items() if v > 1}
    if not duplicates:
        return await m.reply('No extras 🆔 found in your collection.')
    
    duplicate_ids = list(duplicates.keys())
    
    # Prepare response
    txt = f"{u.user.first_name}'s duplicate character IDs:\n\n"
    txt += "\n".join(str(id) for id in duplicate_ids)
    
    await m.reply(txt)