from pyrogram import Client, filters
from ..Database.users import get_all_users
from ..universal_decorator import YxH
import heapq

# Define the image map
image_map = {
    "**Top Miners**": "Images/mtop.jpg",
    "**Top Collectors**": "Images/top.jpg",
    "**Top Crystal Holders**": "Images/ctop.jpg",
}

# Change this function to calculate the sum of gold held by each user
def key_func(user):
    return user.gold  # Assuming 'gold' is the attribute that holds the gold amount

@Client.on_message(filters.command("top"))
@YxH()  # Assuming YxH decorator is correct
async def top(_, m, u):
    users = await get_all_users()  # Get all users
    # This will get the top 10 users based on the amount of gold they hold
    top10 = heapq.nlargest(10, users, key=key_func)
    
    txt = "**Top Miners**"
    txt += "\n\n"

    for x, y in enumerate(top10):
        txt += f"`{x+1}.` **{y.user.first_name}** - `{y.gold}`\n"  # Ensure 'gold' is an existing attribute

    # Get the appropriate image for this category from the image map
    image_path = image_map["**Top Miners**"]

    # Send photo with caption
    await m.reply_photo(
        photo=image_path,
        caption=txt
    )

# Function to calculate the size of the collection
def c_func(user):
    return len(user.collection)  # Ensure 'collection' is a list or collection object

@Client.on_message(filters.command("ctop"))
@YxH()
async def ctop(_, m):
    users = await get_all_users()  # Get all users
    # Get the top 10 users based on the size of their collections
    top10 = heapq.nlargest(10, users, key=c_func)
    
    txt = "**Top Collectors**\n\n"

    for x, y in enumerate(top10):
        txt += f"`{x+1}.` **{y.user.first_name}** - `{len(y.collection)}`\n"  # Ensure 'collection' is iterable

    # Get the appropriate image for this category from the image map
    image_path = image_map["**Top Collectors**"]

    # Send photo with caption
    await m.reply_photo(
        photo=image_path,
        caption=txt
    )

# Function to calculate the amount of crystals
def cr_func(user):
    return user.crystals  # Ensure 'crystals' is an existing attribute    

@Client.on_message(filters.command("crtop"))
@YxH()
async def crtop(_, m, u):
    users = await get_all_users()  # Get all users
    # This will get the top 10 users based on the amount of crystals they hold
    top10 = heapq.nlargest(10, users, key=cr_func)
    
    txt = "**Top Crystal Holders**"
    txt += "\n\n"

    for x, y in enumerate(top10):
        txt += f"`{x+1}.` **{y.user.first_name}** - `{y.crystals}`\n"  # Ensure 'crystals' is an existing attribute

    # Get the appropriate image for this category from the image map
    image_path = image_map["**Top Crystal Holders**"]

    # Send photo with caption
    await m.reply_photo(
        photo=image_path,
        caption=txt
    )