from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from . import get_date, YxH

import time
import asyncio

equipment_data = {
    "Axe": {"emoji": "🪓", "increase": 3, "cost": 10000},
    "Hammer": {"emoji": "🔨", "increase": 7, "cost": 15000},
    "Shovel": {"emoji": "🛠", "increase": 5, "cost": 12000},
    "Pickaxe": {"emoji": "⛏", "increase": 5, "cost": 12000},
    "Bomb": {"emoji": "💣", "increase": 10, "cost": 50000}
}

def equipments_markup(u):
    lis = []
    for x in equipments_data:
        txt = x["emoji"] + " " + x + " "
        txt += "☑️" if x[0].lower() in u.rented_items else str(x["cost"])
        lis.append(InlineKeyboardButton(txt, callback_data=f"{x}_{u.user.id}"))
    return InlineKeyboardMarkup([lis])

@Client.on_message(filters.command("equipments"))
@YxH(private=False)
async def equipments_handler(client: Client, message: Message, user):
    user_id = message.from_user.id
     

    
    keyboard = equipments_markup(user)

    
    await message.reply_text(
        "Select the equipment you want to rent for 15 days:",
        reply_markup=keyboard
    )
    
async def e_cbq(_, q, u):
    data = q.data
    id = u.user.id
    if data.startswith("Axe"):
        if "a" in u.rented_items:
            return await q.answer("You have already rented it.", show_alert=True)
        req = equipment_data["Axe"]["cost"]
        if u.gold < req:
            r = req - u.gold
            return await q.answer("You need `{r}` more gold to rent it.", show_alert=True)
        u.gold -= req
        u.rented_items["a"] = time.time()
        markup = equipments_markup(u)
        await asyncio.gather(
          u.update(),
          q.answer("Rented Successfully.", show_alert=True),
          q.edit_message_reply_markup(reply_markup=markup)
        )