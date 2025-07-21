import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb
from pyrogram.types import CallbackQuery
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from . import YxH, get_anime_character
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
        account = await asyncio.to_thread(telegraph.create_account, short_name=user.first_name)
        if 'error' in account:
            return None, account.get('error')
        telegraph_accounts[user.id] = account
        return account, None
    except Exception as e:
        return None, str(e)

# Function to create PDF for duplicate characters
async def create_pdf_for_duplicates(user, duplicates, file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"{user.first_name}'s Duplicate Characters")
    y -= 30

    c.setFont("Helvetica", 12)
    for dup_id, count in duplicates.items():
        char = await get_anime_character(dup_id)
        if not char:
            continue
        line = f"{char.name} (ID: {char.id}) × {count}"
        if y < 50:
            c.showPage()
            y = height - 50
        c.drawString(50, y, line)
        y -= 20

    c.save()

# Extras (Duplicates) Command using PDF instead of Telegraph
@Client.on_message(filters.command('extras'))
@YxH()
async def find_duplicates(_, m, u):
    user = m.from_user
    coll_dict: dict = u.collection
    if not coll_dict:
        return await m.reply('Your collection is empty.')

    # Find duplicates where count > 1
    duplicates = {k: v for k, v in coll_dict.items() if isinstance(v, int) and v > 1}
    if not duplicates:
        return await m.reply('No extras 🆔 found in your collection.')

    file_path = f"/tmp/{user.id}_duplicates.pdf"
    await create_pdf_for_duplicates(user, duplicates, file_path)

    try:
        await m.reply_document(file_path, caption="📄 Here is your Duplicate Characters list.")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# Uncollected Characters Command (unchanged)
@Client.on_message(filters.command('uncollected'))
@YxH()
async def uncollected_characters(_, m, u):
    markup = ikm([[ikb("Show Uncollected Characters", callback_data="uncollected")]])
    await m.reply(
        "Click the button below to view your uncollected characters.",
        reply_markup=markup
    )