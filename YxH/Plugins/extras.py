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

    # Prepare the message with character names and IDs
    txt = f"{u.user.first_name}'s Duplicate Characters:\n\n"
    buttons = []
    for dup_id in duplicates.keys():
        char = await get_anime_character(dup_id)
        txt += f"• {char.name} (ID: {char.id})\n"
        # Add an inline button to view the character's image
        buttons.append([ikb(f"View {char.name}", callback_data=f"view_char_image|{char.id}")])

    # Reply with the character list and buttons
    await m.reply(txt, reply_markup=ikm(buttons))