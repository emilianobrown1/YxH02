import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb
from . import YxH, get_anime_character
from pyrogram.types import CallbackQuery
from telegraph import Telegraph

from YxH.Database.characters import get_all as get_all_anime_characters

# Initialize the Telegraph object
telegraph = Telegraph()

# Global cache for Telegraph accounts: maps user.id to account data
telegraph_accounts = {}

async def get_telegraph_account(user):
    if user.id in telegraph_accounts:
        return telegraph_accounts[user.id], None
    try:
        # Run the blocking call in a thread
        account = await asyncio.to_thread(telegraph.create_account, short_name=user.first_name)
        if 'error' in account:
            return None, account.get('error')
        telegraph_accounts[user.id] = account
        return account, None
    except Exception as e:
        return None, str(e)

# Function to create a Telegraph page for duplicate characters
async def create_telegraph_page_for_duplicates(user, duplicates):
    account, error = await get_telegraph_account(user)
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
        # Run the blocking create_page call in a thread
        page = await asyncio.to_thread(
            telegraph.create_page,
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
    account, error = await get_telegraph_account(user)
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
        # Run the blocking create_page call in a thread
        page = await asyncio.to_thread(
            telegraph.create_page,
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

    await m.reply(f"Here are your duplicate characters: {telegraph_url}")

# Uncollected Characters Command
@Client.on_message(filters.command('uncollected'))
@YxH()
async def uncollected_characters(_, m, u):
    markup = ikm([[ikb("Show Uncollected Characters", callback_data="uncollected")]])
    await m.reply(
        "Click the button below to view your uncollected characters.",
        reply_markup=markup
    )