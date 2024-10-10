from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb
from . import YxH, get_anime_character
from YxH.Database.characters import get_all as get_all_anime_characters

ITEMS_PER_PAGE = 10

# Extras (Duplicates) Command
@Client.on_message(filters.command('extras'))
@YxH()
async def find_duplicates(_, m, u):
    user = m.from_user  # Fetch the user object from the message
    coll_dict: dict = u.collection
    if not coll_dict:
        return await m.reply('Your collection is empty.')

    # Find duplicates
    duplicates = {k: v for k, v in coll_dict.items() if v > 1}
    if not duplicates:
        return await m.reply('No extras 🆔 found in your collection.')

    # Prepare the message with character names and IDs
    txt = f"{user.first_name}'s Duplicate Characters:\n\n"
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
    all_characters = await get_all_anime_characters()

    if not all_characters:
        return await m.reply("No characters are available.")

    # Filter out characters the user hasn't collected
    uncollected = [char for char in all_characters.values() if char.id not in coll_dict]

    if not uncollected:
        return await m.reply("You have collected all characters!")

    # Start with the first page
    await send_uncollected_page(m, uncollected, 1)

# Function to send a specific page of uncollected characters
async def send_uncollected_page(m, uncollected, page):
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_characters = uncollected[start:end]

    # Prepare the message with uncollected character names and IDs
    txt = f"{m.from_user.first_name}'s Uncollected Characters (Page {page}):\n\n"
    for char in page_characters:
        txt += f"• {char.name} (ID: {char.id})\n"

    # Create pagination buttons
    buttons = []
    if page > 1:
        buttons.append(ikb("Previous", callback_data=f"uncollected_prev_{page}"))
    if end < len(uncollected):
        buttons.append(ikb("Next", callback_data=f"uncollected_next_{page}"))

    # Send the message with inline buttons
    await m.reply(txt, reply_markup=ikm([buttons]) if buttons else None)

# Callback query handler for uncollected pagination
@Client.on_callback_query(filters.regex(r"uncollected_(prev|next)_(\d+)"))
@YxH()
async def uncollected_pagination(_, cq):
    action, current_page = cq.data.split('_')[1:]
    current_page = int(current_page)
    
    coll_dict: dict = cq.from_user.collection
    all_characters = await get_all_anime_characters()

    # Filter out characters the user hasn't collected
    uncollected = [char for char in all_characters.values() if char.id not in coll_dict]

    if action == "next":
        next_page = current_page + 1
        await send_uncollected_page(cq.message, uncollected, next_page)
    elif action == "prev":
        prev_page = current_page - 1
        await send_uncollected_page(cq.message, uncollected, prev_page)

    # Answer the callback query to remove the loading animation
    await cq.answer()