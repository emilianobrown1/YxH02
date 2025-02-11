from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb
from . import YxH, get_anime_character
from pyrogram.types import CallbackQuery
from telegraph import Telegraph
import asyncio

from YxH.Database.characters import get_all as get_all_anime_characters

# Initialize the Telegraph object
telegraph = Telegraph()

# Function to create a Telegraph page for duplicates
async def create_telegraph_page_for_duplicates(user, duplicates):
    # Create a new Telegraph account (optional - use an existing one)
    telegraph.create_account(short_name=user.first_name)

    # Prepare the content for the page
    content = f"<strong>{user.first_name}'s Duplicate Characters:</strong><ul>"
    for dup_id in duplicates.keys():
        char = await get_anime_character(dup_id)
        content += f"<li>{char.name} (ID: {char.id})</li>"
    content += "</ul>"

    # Create the page with the content
    page = telegraph.create_page(
        title=f"{user.first_name}'s Duplicates",
        html_content=content
    )

    return page['url']

# Function to create a Telegraph page for uncollected characters
async def create_telegraph_page_for_uncollected(user, uncollected):
    # Create a new Telegraph account (optional - use an existing one)
    telegraph.create_account(short_name=user.first_name)

    # Prepare the content for the page
    content = f"<strong>{user.first_name}'s Uncollected Characters:</strong><ul>"
    for char in uncollected:
        content += f"<li>{char.name} (ID: {char.id})</li>"
    content += "</ul>"

    # Create the page with the content
    page = telegraph.create_page(
        title=f"{user.first_name}'s Uncollected Characters",
        html_content=content
    )

    return page['url']


# Extras (Duplicates) Command
@Client.on_message(filters.command('extras'))
@YxH()
async def find_duplicates(_, m, u):
    user = m.from_user  # Fetch the user object from the message
    coll_dict: dict = u.collection
    if not coll_dict:
        return await m.reply('Your collection is empty.')

    # Find duplicates where count > 1
    duplicates = {k: v for k, v in coll_dict.items() if isinstance(v, int) and v > 1}
    if not duplicates:
        return await m.reply('No extras 🆔 found in your collection.')

    # Generate Telegraph page URL for duplicates
    telegraph_url = await create_telegraph_page_for_duplicates(user, duplicates)

    # Send the Telegraph page link to the user
    await m.reply(f"Here are your duplicate characters: {telegraph_url}")



@Client.on_message(filters.command('uncollected'))
@YxH()
async def uncollected_characters(_, m, u):
    # Use the imported aliases ikm and ikb
    markup = ikm(
        [[ikb("Show Uncollected Characters", callback_data="uncollected")]]
    )
    await m.reply(
        "Click the button below to view your uncollected characters.",
        reply_markup=markup
    )