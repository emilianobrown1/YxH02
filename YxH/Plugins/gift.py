from pyrogram import Client, filters
from . import YxH, get_date, get_user, ikm, ikb
import math

@Client.on_message(filters.command("xgift"))
@YxH(min_old=3)
async def xgift(_, m, u):
    if u.gifts == 0:
        return await m.reply("You have no gifts left.\n\nHowever you can buy them using /xgifts.")
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
    u.gifts -= 1
    await t.update()
    await u.update()
    await m.reply(f"Successfully gifted the character of ID `{id}` to {t.user.first_name}.\n\nGifts left for today: `{u.gifts}`.")
    await _.send_message(t.user.id, f"{u.user.first_name} has gifted you the character of ID `{id}`.")

def markup(user_id, gifts):
    return ikm([[ikb("Buy", callback_data=f"gifts|{gifts}_{user_id}")], [ikb("Close", callback_data=f"close_{user_id}")]])

@Client.on_message(filters.command("xgifts"))
@YxH(min_old=3)
async def xgifts(_, m, u):
    try:
        count = int(m.text.split()[1])
    except:
        return await m.reply(f"Usage: /xgifts [count]\n\nYou have: `{u.gifts}`.")
    cost = math.ceil(count/5)
    txt = f"Gifts: `{count}`\nCost: `{cost}` Crystals\n\nYou have: `{u.gifts}`."
    await m.reply(txt, reply_markup=markup(u.user.id, count))

def close(user_id):    
    return ikm([[ikb("Close", callback_data=f"close_{user_id}")]])

async def gifts_cbq(_, q, u):
    count = int(q.data.split("_")[0].split("|")[1])
    cost = math.ceil(count/5)
    if u.crystals < cost:
        return await q.answer(f"You need {cost-u.crystals} crystals more to buy.")
    u.crystals -= cost
    u.gifts += count
    txt = f"Successfully bought `{count}` gifts for `{cost}` crystals.\n\nYou have: `{u.gifts}`."
    await u.update()
    await q.answer()
    await q.edit_message_text(txt, reply_markup=close(u.user.id))
