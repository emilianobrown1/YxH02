from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb
from . import YxH, get_anime_character
from YxH.Database.characters import get_all_anime_characters  # Adjust path as needed

# Extras (Duplicates) Command
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
    txt = f"{u.first_name}'s Duplicate Characters:\n\n"
    for dup_id in duplicates.keys():
        char = await get_anime_character(dup_id)
        txt += f"• {char.name} (ID: {char.id})\n"

    # Single inline button to view all duplicates
    buttons = [[ikb("View Duplicates", callback_data="view_all_duplicates")]]

    # Reply with the character list and the inline button
    await m.reply(txt, reply_markup=ikm(buttons))

# Uncollected Characters Command
@Client.on_message(filters.command('uncollected'))
@YxH()
async def uncollected_characters(_, m, u):
    coll_dict: dict = u.collection
    all_characters = await get_all_anime_characters()  # Assuming this fetches all available characters

    if not all_characters:
        return await m.reply("No characters are available.")

    # Filter out characters the user hasn't collected
    uncollected = [char for char in all_characters if char["id"] not in coll_dict]

    if not uncollected:
        return await m.reply("You have collected all characters!")

    # Prepare the message with uncollected character names and IDs
    txt = f"{u.first_name}'s Uncollected Characters:\n\n"
    for char in uncollected:
        txt += f"• {char['name']} (ID: {char['id']})\n"

    # Single inline button to view uncollected characters
    buttons = [[ikb("View Uncollected", callback_data="view_uncollected")]]

    # Reply with the uncollected character list and the inline button
    await m.reply(txt, reply_markup=ikm(buttons))

# Callback handler for viewing duplicates (extras)
@Client.on_callback_query(filters.regex("view_all_duplicates"))
async def view_duplicates(_, callback_query):
    u = callback_query.from_user  # Get user info from callback query
    coll_dict: dict = u.collection

    # Find duplicates
    duplicates = {k: v for k, v in coll_dict.items() if v > 1}
    
    if not duplicates:
        return await callback_query.answer("No extras found!", show_alert=True)

    # Prepare the message with character names and IDs
    txt = f"{u.first_name}'s Duplicate Characters:\n\n"
    for dup_id in duplicates.keys():
        char = await get_anime_character(dup_id)
        txt += f"• {char.name} (ID: {char.id})\n"

    # Edit the message to show duplicates
    await callback_query.message.edit_text(txt)

# Callback handler for viewing uncollected characters
@Client.on_callback_query(filters.regex("view_uncollected"))
async def view_uncollected_characters(_, callback_query):
    u = callback_query.from_user  # Get user info from callback query
    coll_dict: dict = u.collection
    all_characters = await get_all_anime_characters()  # Assuming this fetches all characters

    # Filter out characters the user hasn't collected
    uncollected = [char for char in all_characters if char["id"] not in coll_dict]

    if not uncollected:
        return await callback_query.answer("You have collected all characters!", show_alert=True)

    # Prepare the message with uncollected character names and IDs
    txt = f"{u.first_name}'s Uncollected Characters:\n\n"
    for char in uncollected:
        txt += f"• {char['name']} (ID: {char['id']})\n"

    # Edit the message to show uncollected characters
    await callback_query.message.edit_text(txt)