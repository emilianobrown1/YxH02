import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from . import YxH, get_anime_character
from telegraph import Telegraph
from YxH.Database.characters import get_all as get_all_anime_characters

# Initialize the Telegraph object
telegraph = Telegraph()
telegraph_accounts = {}  # user.id → Telegraph account


# ------------------- Telegraph Account Setup -------------------
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


# ------------------- PDF Creation for Duplicates -------------------
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


# ------------------- Telegraph Page for Uncollected -------------------
async def create_telegraph_page_for_uncollected(user, uncollected):
    account, error = await get_telegraph_account(user)
    if error:
        return None

    content = f"<strong>{user.first_name}'s Uncollected Characters:</strong><ul>"
    for char in uncollected:
        if not char:
            continue
        content += f"<li>{char.name} (ID: {char.id})</li>"
    content += "</ul>"

    try:
        page = await asyncio.to_thread(
            telegraph.create_page,
            title=f"{user.first_name}'s Uncollected Characters",
            html_content=content
        )
        if 'error' in page:
            return None
        return page.get('url')
    except Exception:
        return None


# ------------------- /extras Command (PDF version) -------------------
@Client.on_message(filters.command('extras'))
@YxH()
async def find_duplicates(_, m, u):
    user = m.from_user
    coll_dict: dict = u.collection
    if not coll_dict:
        return await m.reply('Your collection is empty.')

    # Find characters with more than 1 copy
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


# ------------------- /uncollected Command (Telegraph version) -------------------
@Client.on_message(filters.command('uncollected'))
@YxH()
async def uncollected_characters(_, m, u):
    markup = ikm([[ikb("Show Uncollected Characters", callback_data="uncollected")]])
    await m.reply(
        "Click the button below to view your uncollected characters.",
        reply_markup=markup
    )