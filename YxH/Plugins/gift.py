from pyrogram import Client, filters
from . import YxH, get_date, get_user, get_date

@Client.on_message(filters.command("xgift"))
@YxH(min_old=3)
async def xgift(_, m, u):
    date = get_date()
    gifts = u.gifts_sent.get(date, 0)
    if gifts >= 5:
        return await m.reply("You have reached the maximum limit of gifting for today.")
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply("Reply to an user.")
    t = await get_user(m.reply_to_message.from_user.id)
    if not t:
        return await m.reply("Replied user is not a player.")
    try:
        id = int(m.text.split()[1])
    except:
        return await m.reply("Usage: /xgift [character id]")
    if not id in u.collection:
        return await m.reply("You do not own this character.")
    if u.collection[id] == 1:
        u.collection.pop(id)
    else:
        u.collection[id] -= 1
    t.collection[id] = t.collection.get(id, 0) + 1
    u.gifts_sent[date] = gifts + 1
    await t.update()
    await u.update()
    await m.reply(f"Successfully gifted the character of ID `{id}` to {t.user.first_name}.\n\nGifts left for today: `{4-gifts}`.")
    await _.send_message(t.user.id, f"{u.user.first_name} has gifted you the character of ID `{id}`.")