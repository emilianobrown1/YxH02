from pyrogram.types import InputMediaPhoto
from pyrogram import Client, filters
from . import YxH, get_date, get_user, ikm, ikb

@Client.on_message(filters.command("xbarracks"))
async def xbarracks(_, m, u):
    try:
        count = int(m.text.split()[1])
    except:
        return await m.reply(
            f"Usage: /xbarracks [count]\n\nYou have: {u.barracks} barracks."
        )
    
    cost = count * 50
    txt = ''

    if count > 4:
        count = 4
        cost = count * 50
        txt += "You can only purchase up to 4 barracks.\n\n"

    txt += f"Barracks: {count}\nCost: {cost} Crystals\n\nYou have: {u.barracks} barracks."
    await m.reply_photo(
        photo="Images/barrack.jpg",  # Replace with the actual image path or URL
        caption=txt,
        reply_markup=barrack_markup(u.user.id, count)
    )


def barrack_markup(user_id, count):
    return ikm([[ikb(f"Buy {count} Barracks", callback_data=f"barrack_{user_id}|{count}")]])


def close(user_id):
    return ikm([[ikb("Close", callback_data=f"close_{user_id}")]])


async def barrack_cbq(_, q, u):
    count = int(q.data.split("_")[0].split("|")[1])
    cost = count * 50

    if count > 4:
        count = 4
        cost = count * 50

    if u.crystals < cost:
        return await q.answer(
            f"You need {cost - u.crystals} more crystals to buy.",
            show_alert=True
        )

    u.crystals -= cost
    u.barracks += count
    txt = f"Successfully bought {count} barracks for {cost} crystals.\n\nYou have: {u.barracks} barracks."
    await u.update()
    await q.answer()
    await q.edit_message_text(txt, reply_markup=close(u.user.id))
