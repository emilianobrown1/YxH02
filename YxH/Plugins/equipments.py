from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from . import get_date, YxH

import time
import asyncio

def get_time(sec):
    days = int(sec/86400)
    hours = int(sec/3600)
    if days == 0 and hours == 0:
        return f"{int(sec/60)}m"
    if days == 0:
        return f"{hours}h"
    if hours == 0:
        return f"{days}d"
    return f"{days}d {hours}h"
        
async def check_expiry(u):
    to_rem = []
    for x in u.rented_items:
        if int(time.time() - u.rented_items[x]) >= 15 * 86400:
            to_rem.append(x)
    for y in to_rem:
        u.rented_items.pop(y)
    await u.update()

equipment_data = {
    "Axe": {"emoji": "🪓", "increase": 3, "cost": 10000},
    "Hammer": {"emoji": "🔨", "increase": 7, "cost": 15000},
    "Shovel": {"emoji": "🛠", "increase": 5, "cost": 12000},
    "Pickaxe": {"emoji": "⛏", "increase": 5, "cost": 12000},
    "Bomb": {"emoji": "💣", "increase": 10, "cost": 50000}
}

def equipments_markup(u):
    lis = []
    for x in equipment_data:
        txt = equipment_data[x]["emoji"] + " " + x + " "
        txt += f"☑️, {get_time((15*86400)-int(time.time()-u.rented_items[x[0].lower()]))}" if x[0].lower() in u.rented_items else "- " + str(equipment_data[x]["cost"])
        lis.append([InlineKeyboardButton(txt, callback_data=f"{x}_{u.user.id}")])
    return InlineKeyboardMarkup(lis)

@Client.on_message(filters.command("equipments"))
@YxH(private=False)
async def equipments_handler(client: Client, message: Message, user):
    await check_expiry(user)
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
    elif data.startswith("Hammer"):
        if "h" in u.rented_items:
            return await q.answer("You have already rented it.", show_alert=True)
        req = equipment_data["Hammer"]["cost"]
        if u.gold < req:
            r = req - u.gold
            return await q.answer("You need `{r}` more gold to rent it.", show_alert=True)
        u.gold -= req
        u.rented_items["h"] = time.time()
        markup = equipments_markup(u)
        await asyncio.gather(
          u.update(),
          q.answer("Rented Successfully.", show_alert=True),
          q.edit_message_reply_markup(reply_markup=markup)
        )
    elif data.startswith("Shovel"):
        if "s" in u.rented_items:
            return await q.answer("You have already rented it.", show_alert=True)
        req = equipment_data["Shovel"]["cost"]
        if u.gold < req:
            r = req - u.gold
            return await q.answer("You need `{r}` more gold to rent it.", show_alert=True)
        u.gold -= req
        u.rented_items["s"] = time.time()
        markup = equipments_markup(u)
        await asyncio.gather(
          u.update(),
          q.answer("Rented Successfully.", show_alert=True),
          q.edit_message_reply_markup(reply_markup=markup)
        )
    elif data.startswith("Pickaxe"):
        if "p" in u.rented_items:
            return await q.answer("You have already rented it.", show_alert=True)
        req = equipment_data["Pickaxe"]["cost"]
        if u.gold < req:
            r = req - u.gold
            return await q.answer("You need `{r}` more gold to rent it.", show_alert=True)
        u.gold -= req
        u.rented_items["p"] = time.time()
        markup = equipments_markup(u)
        await asyncio.gather(
          u.update(),
          q.answer("Rented Successfully.", show_alert=True),
          q.edit_message_reply_markup(reply_markup=markup)
        )
    elif data.startswith("Bomb"):
        if "b" in u.rented_items:
            return await q.answer("You have already rented it.", show_alert=True)
        req = equipment_data["Bomb"]["cost"]
        if u.gold < req:
            r = req - u.gold
            return await q.answer("You need `{r}` more gold to rent it.", show_alert=True)
        u.gold -= req
        u.rented_items["b"] = time.time()
        markup = equipments_markup(u)
        await asyncio.gather(
          u.update(),
          q.answer("Rented Successfully.", show_alert=True),
          q.edit_message_reply_markup(reply_markup=markup)
        )