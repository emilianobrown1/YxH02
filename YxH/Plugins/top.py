from pyrogram import Client, filters
from ..Database.users import get_all_users
from ..universal_decorator import YxH
import heapq
from . import YxH
from ..load_attr import load_attr

TOP_MINERS_IMAGE_PATH = "Images/mtop.jpg"
TOP_COLLECTORS_IMAGE_PATH = "Images/top.jpg"
TOP_CRYSTAL_HOLDERS_IMAGE_PATH = "Images/ctop.jpg"

# Function to calculate the amount of gold held by each user
def key_func(user):
    return user.gold  # Assuming 'gold' is the attribute that holds the gold amount

@Client.on_message(filters.command("top"))
@YxH()
async def top(client, m, u):
    users = await get_all_users()
    # Get the top 10 users based on the amount of gold they hold
    top10 = heapq.nlargest(10, users, key=key_func)
    txt = "Top Miners\n\n"
    for x, y in enumerate(top10):
        user_info = await client.get_users(y.user_id)  # Dynamically fetch user info
        txt += f"{x+1}. {user_info.first_name} ({y.user_id}) - {y.gold}\n"
    with open(TOP_MINERS_IMAGE_PATH, "rb") as image_file:
        await m.reply_photo(image_file, caption=txt)

# Function to calculate the size of the collection of each user
def c_func(user):
    return len(user.collection)

@Client.on_message(filters.command("ctop"))
@YxH()
async def ctop(client, m, u):
    users = await get_all_users()
    # Get the top 10 users based on the collection size
    top10 = heapq.nlargest(10, users, key=c_func)
    txt = "Top Collectors\n\n"
    for x, y in enumerate(top10):
        user_info = await client.get_users(y.user_id)  # Dynamically fetch user info
        txt += f"{x+1}. {user_info.first_name} ({y.user_id}) - {len(y.collection)}\n"
    with open(TOP_COLLECTORS_IMAGE_PATH, "rb") as image_file:
        await m.reply_photo(image_file, caption=txt)

# Function to calculate the number of crystals held by each user
def cr_func(user):
    return user.crystals  # Assuming 'crystals' is the attribute that holds the crystals amount

@Client.on_message(filters.command("crtop"))
@YxH()
async def crtop(client, m, u):
    users = await get_all_users()
    # Get the top 10 users based on the amount of crystals they hold
    top10 = heapq.nlargest(10, users, key=cr_func)
    txt = "Top Crystal Holders\n\n"
    for x, y in enumerate(top10):
        user_info = await client.get_users(y.user_id)  # Dynamically fetch user info
        txt += f"{x+1}. {user_info.first_name} ({y.user_id}) - {y.crystals}\n"
    with open(TOP_CRYSTAL_HOLDERS_IMAGE_PATH, "rb") as image_file:
        await m.reply_photo(image_file, caption=txt)