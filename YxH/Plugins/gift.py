from pyrogram import Client, filters
from . import YxH, get_date, get_user

@Client.on_message(filters.command("xgift"))
@YxH()
async def xgift(_, m, u):
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply("Reply to an user.")
    t = await get_user(m.reply_to_message.from_user.id)
    if not t:
        return await m.reply("Replied user is not a player.")
    try:
        id = int(m.text.split()[1])
    except:
        return await m.reply("Usage: /xgift [character id]")
    have = u.collection.get(id, 0)
    if have == 0:
        return await m.reply("You do not own this character.")