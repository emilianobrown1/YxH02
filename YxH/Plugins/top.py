from pyrogram import Client, filters
from ..Database.users import get_all_users
from ..universal_decorator import YxH
import heapq
from ..load_attr import load_attr
    
def key_func(user):
    try:
        return sum([user.mine[x] for x in user.mine])
    except AttributeError:
        user = await load_attr(user.user.id)
        return sum([user.mine[x] for x in user.mine])

@Client.on_message(filters.command("top"))
@YxH()
async def top(_, m, u):
    users = await get_all_users()
    top10 = heapq.nlargest(10, users, key=key_func)
    txt = "**Top Miners**"
    txt += "\n\n"
    for x, y in emumerate(top10):
        txt += f"`{x+1}. **{y.user.first_name}**\n"
    await m.reply(txt)