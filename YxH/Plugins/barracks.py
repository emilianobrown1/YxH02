from pyrogram.types import InputMediaPhoto
from pyrogram import Client, filters
from . import YxH, get_date, get_user, ikm, ikb

@Client.on_message(filters.command("xbarracks"))
@YxH()
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
        "Images/barrack.jpg",  # Replace with the actual image path or URL
        caption=txt,
        reply_markup=barrack_markup(u.user.id, count)
    )


def barrack_markup(user_id, count):
    return ikm([[ikb(f"Buy {count} Barracks", callback_data=f"barrack_{user_id}|{count}")]])


def close(user_id):
    return ikm([[ikb("Close", callback_data=f"close_{user_id}")]])


@Client.on_callback_query(filters.regex(r"^barrack_\d+\|\d+$"))
@YxH()
async def barrack_cbq(_, q, u):
    # Parse callback data
    try:
        action, data = q.data.split("_", 1)
        user_id, count = map(int, data.split("|"))
    except ValueError:
        return await q.answer("Invalid data format.", show_alert=True)

    # Validate user ownership of the callback
    if user_id != u.user.id:
        return await q.answer("This action is not for you.", show_alert=True)

    # Calculate cost and validate count
    max_count = 4
    count = min(count, max_count)  # Cap the count at the max limit
    cost = count * 50

    # Check if the user has enough crystals
    if u.crystals < cost:
        return await q.answer(
            f"You need {cost - u.crystals} more crystals to buy.",
            show_alert=True,
        )

    # Deduct crystals and update barracks
    u.crystals -= cost
    u.barracks += count
    await u.update()

    # Notify user of the purchase
    txt = f"Successfully bought {count} barracks for {cost} crystals.\n\nYou now have: {u.barracks} barracks."
    await q.answer()
    await q.edit_message_text(txt, reply_markup=close_markup(u.user.id))
