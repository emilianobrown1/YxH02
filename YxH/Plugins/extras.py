from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb
from . import YxH, get_anime_character
from pyrogram.types import CallbackQuery
from telegraph import Telegraph
import asyncio

from YxH.Database.characters import get_all as get_all_anime_characters

# Initialize the Telegraph object
telegraph = Telegraph()

async def create_telegraph_account(user):
    try:
        result = telegraph.create_account(short_name=user.first_name)
        if 'error' in result:
            return None, result.get('error')
        return result, None
    except Exception as e:
        return None, str(e)

# Function to create a Telegraph page for duplicate characters
async def create_telegraph_page_for_duplicates(user, duplicates):
    # Create Telegraph account and check for errors
    account, error = await create_telegraph_account(user)
    if error:
        return None, f"Failed to create Telegraph account: {error}"

    # Prepare the HTML content for the page
    content = f"<strong>{user.first_name}'s Duplicate Characters:</strong><ul>"
    for dup_id, count in duplicates.items():
        char = await get_anime_character(dup_id)
        if not char:
            continue
        content += f"<li>{char.name} (ID: {char.id})</li>"
    content += "</ul>"

    try:
        # Adding a slight delay to avoid hitting rate limits
        await asyncio.sleep(1)
        page = telegraph.create_page(
            title=f"{user.first_name}'s Duplicates",
            html_content=content
        )
        if 'error' in page:
            return None, f"Telegraph page error: {page.get('error')}"
        return page.get('url'), None
    except Exception as e:
        return None, f"Telegraph page creation failed: {e}"

# Function to create a Telegraph page for uncollected characters
async def create_telegraph_page_for_uncollected(user, uncollected):
    # Create Telegraph account and check for errors
    account, error = await create_telegraph_account(user)
    if error:
        return None, f"Failed to create Telegraph account: {error}"

    # Prepare the HTML content for the page
    content = f"<strong>{user.first_name}'s Uncollected Characters:</strong><ul>"
    for char in uncollected:
        if not char:
            continue
        content += f"<li>{char.name} (ID: {char.id})</li>"
    content += "</ul>"

    try:
        # Adding a slight delay to avoid hitting rate limits
        await asyncio.sleep(1)
        page = telegraph.create_page(
            title=f"{user.first_name}'s Uncollected Characters",
            html_content=content
        )
        if 'error' in page:
            return None, f"Telegraph page error: {page.get('error')}"
        return page.get('url'), None
    except Exception as e:
        return None, f"Telegraph page creation failed: {e}"

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
    telegraph_url, error = await create_telegraph_page_for_duplicates(user, duplicates)
    if error:
        return await m.reply(f"Error: {error}")

    # Send the Telegraph page link to the user
    await m.reply(f"Here are your duplicate characters: {telegraph_url}")

# Uncollected Characters Command
@Client.on_message(filters.command('uncollected'))
@YxH()
async def uncollected_characters(_, m, u):
    markup = ikm(
        [[ikb("Show Uncollected Characters", callback_data="uncollected")]]
    )
    await m.reply(
        "Click the button below to view your uncollected characters.",
        reply_markup=markup
    )