from pyrogram import Client, filters
from . import YxH, get_anime_character
from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb

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

    # Prepare response text with character names and IDs
    txt = f"{u.user.first_name}'s duplicate characters:\n\n"
    buttons = []
    for dup_id in duplicate_ids:
        char = await get_anime_character(dup_id)  # Fetch character info
        txt += f"• {char.name} (ID: {char.id})\n"
        # Create buttons to view details of each duplicate character
        buttons.append([ikb(f"View {char.name}", callback_data=f"view|0|{char.id}")])

    # Inline keyboard markup for viewing each character
    reply_markup = ikm(buttons)

    # Reply with the list of duplicates and the inline buttons
    await m.reply(txt, reply_markup=reply_markup)