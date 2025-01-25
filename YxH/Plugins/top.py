from pyrogram import Client, filters
from ..Database.users import get_all_users
from ..universal_decorator import YxH
import heapq

# File paths for images
TOP_MINERS_IMAGE_PATH = "Images/mtop.jpg"
TOP_COLLECTORS_IMAGE_PATH = "Images/top.jpg"
TOP_CRYSTAL_HOLDERS_IMAGE_PATH = "Images/ctop.jpg"

# Helper functions to extract key attributes
def key_func(user):
    return getattr(user, "gold", 0)  # Safely fetch the gold amount, default to 0

def c_func(user):
    return len(getattr(user, "collection", []))  # Safely get the collection size

def cr_func(user):
    return getattr(user, "crystals", 0)  # Safely fetch the crystals amount, default to 0


@Client.on_message(filters.command("top"))
@YxH()
async def top(_, m, u):
    users = await get_all_users()
    # Get the top 10 users based on gold
    top10 = heapq.nlargest(10, users, key=key_func)

    # Generate the message text
    txt = "**Top Miners**\n\n"
    for rank, user in enumerate(top10, start=1):
        name = getattr(user, "first_name", "Unknown")  # Safely get the user's name
        gold = key_func(user)
        txt += f"`{rank}.` **{name}** - `{gold}` 🎐\n"  # Using 🎐 for gold (gim)

    # Send the response with the image
    try:
        with open(TOP_MINERS_IMAGE_PATH, "rb") as image_file:
            await m.reply_photo(image_file, caption=txt)
    except FileNotFoundError:
        await m.reply_text(txt)  # Fallback to plain text if the image is missing


@Client.on_message(filters.command("ctop"))
@YxH()
async def ctop(_, m, u):
    users = await get_all_users()
    # Get the top 10 users based on collection size
    top10 = heapq.nlargest(10, users, key=c_func)

    # Generate the message text
    txt = "**Top Collectors**\n\n"
    for rank, user in enumerate(top10, start=1):
        name = getattr(user, "first_name", "Unknown")  # Safely get the user's name
        collection_size = c_func(user)
        txt += f"`{rank}.` **{name}** - `{collection_size}` 📚\n"  # Using 📚 for collection

    # Send the response with the image
    try:
        with open(TOP_COLLECTORS_IMAGE_PATH, "rb") as image_file:
            await m.reply_photo(image_file, caption=txt)
    except FileNotFoundError:
        await m.reply_text(txt)  # Fallback to plain text if the image is missing


@Client.on_message(filters.command("crtop"))
@YxH()
async def crtop(_, m, u):
    users = await get_all_users()
    # Get the top 10 users based on crystals
    top10 = heapq.nlargest(10, users, key=cr_func)

    # Generate the message text
    txt = "**Top Crystal Holders**\n\n"
    for rank, user in enumerate(top10, start=1):
        name = getattr(user, "first_name", "Unknown")  # Safely get the user's name
        crystals = cr_func(user)
        txt += f"`{rank}.` **{name}** - `{crystals}` 💜\n"  # Using 💜 for crystals (Purple)

    # Send the response with the image
    try:
        with open(TOP_CRYSTAL_HOLDERS_IMAGE_PATH, "rb") as image_file:
            await m.reply_photo(image_file, caption=txt)
    except FileNotFoundError:
        await m.reply_text(txt)  # Fallback to plain text if the image is missing