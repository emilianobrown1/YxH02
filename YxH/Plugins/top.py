from pyrogram import Client, filters
from ..Database.users import get_all_users
from ..universal_decorator import YxH
import heapq
from ..load_attr import load_attr

# Change this function to calculate the sum of gold held by each user
def key_func(user):
    return user.gold  # Assuming 'gold' is the attribute that holds the gold amount

@Client.on_message(filters.command("top"))
@YxH()
async def top(_, m, u):
    users = await get_all_users()
    # This will get the top 10 users based on the amount of gold they hold
    top10 = heapq.nlargest(10, users, key=key_func)
    txt = "**Top Miner**"
    txt += "\n\n"
    for x, y in enumerate(top10):
        txt += f"`{x+1}.` **{y.user.first_name}** - `{y.gold}`\n"  # Display the gold amount
    await m.reply(txt)
    
