from pyrogram import Client, filters
from ..Database.users import get_all_users
from ..universal_decorator import YxH
import heapq
from ..load_attr import load_attr
    
def key_func(user):
    return sum([user.mine[x] for x in user.mine])
        
@Client.on_message(filters.command("top"))
@YxH()
async def top(_, m, u):
    users = await get_all_users()
    top10 = heapq.nlargest(10, users, key=key_func)
    txt = "**Top Miners**"
    txt += "\n\n"
    for x, y in enumerate(top10):
        txt += f"`{x+1}.` **{y.user.first_name}** - `{sum([y.mine[z] for z in y.mine])}`\n"
    await m.reply(txt)