from pyrogram import Client, filters
from ..Database.users import get_all_users
from ..universal_decorator import YxH
import heapq

# Change this function to calculate the sum of gold held by each user
def key_func(user):
    return user.gold  # Assuming 'gold' is the attribute that holds the gold amount

def get_display_name(user):
    """
    Get a display name for the user.
    If first_name or username is not available, fallback to user_id.
    """
    # Use user.user to get the name information
    name = getattr(user.user, "first_name", None) or getattr(user.user, "username", None) or f"User {user.user.id}"
    return name

@Client.on_message(filters.command("top"))
@YxH()
async def top(_, m, u):
    users = await get_all_users()
    # This will get the top 10 users based on the amount of gold they hold
    top10 = heapq.nlargest(10, users, key=key_func)
    txt = "**Top Miners**"
    txt += "\n\n"
    for x, y in enumerate(top10):
        # Use get_display_name function to correctly handle name extraction
        txt += f"`{x+1}.` **{get_display_name(y)}** - `{y.gold}`\n"  # Display the gold amount
    await m.reply(txt)

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
        # Use get_display_name function to correctly handle name extraction
        txt += f"`{x+1}.` **{get_display_name(y)}** - `{len(y.collection)}`\n"  # Display the collection size
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
        # Use get_display_name function to correctly handle name extraction
        txt += f"`{x+1}.` **{get_display_name(y)}** - `{y.crystals}`\n"  # Display the crystals amount
    await m.reply(txt)