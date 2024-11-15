from pyrogram import Client, filters
from ..Database.users import get_all_users
from ..universal_decorator import YxH
import heapq
from . import YxH
from ..load_attr import load_attr

TOP_MINERS_IMAGE_PATH = "Images/mtop.jpg"

# Change this function to calculate the sum of gold held by each user
def key_func(user):
    return user.gold  # Assuming 'gold' is the attribute that holds the gold amount

@Client.on_message(filters.command("top"))
@YxH()
async def top(_, m, u):
    users = await get_all_users()
    # This will get the top 10 users based on the amount of gold they hold
    top10 = heapq.nlargest(10, users, key=key_func)
    txt = "**Top Miners**"
    txt += "\n\n"
    for x, y in enumerate(top10):
        txt += f"`{x+1}.` **{y.user.first_name}** - `{y.gold}`\n"  # Display the gold amount
    with open(TOP_MINERS_IMAGE_PATH, "rb") as image_file:
        await m.reply_photo(image_file, caption=txt)

def c_func(user):
    return len(user.collection)

@Client.on_message(filters.command("ctop"))
@YxH()
async def ctop(_, m, u):
    users = await get_all_users()
    # This will get the top 10 users based on the amount of gold they hold
    top10 = heapq.nlargest(10, users, key=c_func)
    txt = "**Top Collectors**"
    txt += "\n\n"
    for x, y in enumerate(top10):
        txt += f"`{x+1}.` **{y.user.first_name}** - `{len(y.collection)}`\n"  # Display the gold amount
    await m.reply(txt)

def cr_func(user):
    return user.crystals  # Assuming 'crystals' is the attribute that holds the crystals amount    
@Client.on_message(filters.command("crtop"))
@YxH()
async def crtop(_, m, u):
    users = await get_all_users()
    # This will get the top 10 users based on the amount of crystals they hold
    top10 = heapq.nlargest(10, users, key=cr_func)
    txt = "**Top Crystal Holders**"
    txt += "\n\n"
    for x, y in enumerate(top10):
        txt += f"`{x+1}.` **{y.user.first_name}** - `{y.crystals}`\n"  # Display the crystals amount
    await m.reply(txt)

