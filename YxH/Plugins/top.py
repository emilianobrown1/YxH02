from pyrogram import Client, filters
from ..Database.users import get_all_users
from ..universal_decorator import YxH
import heapq
from . import YxH
from ..load_attr import load_attr


@Client.on_message(filters.command("top"))
@YxH()
async def top(_, m, u):
    users = await get_all_users()
    # This will get the top 10 users based on the amount of gold they hold
    top10 = heapq.nlargest(10, users, key=key_func)
    txt = "Top Miners\n\n"
    for x, y in enumerate(top10):
        txt += f"{x+1}. {y.first_name} - {y.gold}\n"  # Access 'first_name' directly
    with open(TOP_MINERS_IMAGE_PATH, "rb") as image_file:
        await m.reply_photo(image_file, caption=txt)

@Client.on_message(filters.command("ctop"))
@YxH()
async def ctop(_, m, u):
    users = await get_all_users()
    # This will get the top 10 users based on the collection size
    top10 = heapq.nlargest(10, users, key=c_func)
    txt = "Top Collectors\n\n"
    for x, y in enumerate(top10):
        txt += f"{x+1}. {y.first_name} - {len(y.collection)}\n"  # Access 'first_name' directly
    with open(TOP_COLLECTORS_IMAGE_PATH, "rb") as image_file:
        await m.reply_photo(image_file, caption=txt)

@Client.on_message(filters.command("crtop"))
@YxH()
async def crtop(_, m, u):
    users = await get_all_users()
    # This will get the top 10 users based on the amount of crystals they hold
    top10 = heapq.nlargest(10, users, key=cr_func)
    txt = "Top Crystal Holders\n\n"
    for x, y in enumerate(top10):
        txt += f"{x+1}. {y.first_name} - {y.crystals}\n"  # Access 'first_name' directly
    with open(TOP_CRYSTAL_HOLDERS_IMAGE_PATH, "rb") as image_file:
        await m.reply_photo(image_file, caption=txt)