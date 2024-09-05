from pyrogram import Client, filters
from . import YxH, grt
from pyrogram.types import (
    InlineKeyboardMarkup as ikm,
    InlineKeyboardButton as ikb
)
import time

shields = {
    "Gold": [5000000, 24],
    "Silver": [300000, 12],
    "Iron": [100000, 8]
}

def build_markup(user_id):
    lis = []
    for x in shields:
        lis.append([ikb(f"{x} ({shields[x][1]}h) - {shields[x][0]} Gold", callback_data=f"shield|{x}_{user_id}")])
    lis.append([ikb("Close", callback_data=f"close_{user_id}")])
    return ikm(lis)

@Client.on_message(filters.command("shield"))
@YxH(main_only=True)
async def sh(_, m, u):
    if u.shield:
        if int(time.time()-u.shield[1]) > u.shield[0]:
            u.shield = []
    if u.shield:
        left = u.shield[0] - int(time.time()-u.shield[1])
        return await m.reply(f"You already having a shield equipped and will be expired after `{grt(left)}`.")
    markup = build_markup(u.user.id)
    await m.reply("**Shields Store**", reply_markup=markup)
    
async def shield_cbq(_, q, u):
    if u.shield:
        if int(time.time()-u.shield[1]) > u.shield[0]:
            u.shield = []
    if u.shield:
        left = u.shield[0] - int(time.time()-u.shield[1])
        await q.answer(f"You already having a shield equipped and will be expired after {grt(left)}.", show_alert=True)
        return await q.message.delete()
    shield_name = q.data.split("_")[0].split("|")[1]
    shield_info = shields[shield_name]
    need = shield_info[0] - u.gold
    if need > 0:
        return await q.answer(f"You need {need} more gold.", show_alert=True)
    u.gold -= shield_info[0]
    u.shield = [shield_info[1]*3600, time.time()]
    await u.update()
    ma = ikm([[ikb("Close", callback_data=f"close_{u.user.id}")]])
    await q.answer()
    return await q.edit_message_text(f"Done, You have equipped **{shield_name}** Shield for `{shield_info[1]}` Hours.", reply_markup=ma)