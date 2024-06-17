from pyrogram import Client, filters
from . import YxH, grt
from pyrogram.types import (
    InlineKeyboardMarkup as ikm,
    InlineKeyboardButton as ikb
)
import time

shields = {
    "Gold": [500000000, 24],
    "Silver": [300000000, 12],
    "Iron": [100000000, 8]
}

def build_markup(user_id):
    lis = []
    for x in shields:
        lis.append(ikb(f"{x} ({shields[x][1]}h) - {shields[x][1]} Gold"))
    lis.append(ikb("Close", callback_data=f"close_{user_id}"))
    return ikm([lis])

@Client.on_message(filters.command("shield"))
@YxH()
async def sh(_, m, u):
    if t.shield:
        if int(time.time()-t.shield[1]) > t.shield[0]:
            t.shield = []
    if t.shield:
        left = t.shield[0] - int(time.time()-t.shield[1])
        return await m.reply(f"You already having a shield equipped and will be expired after `{grt(left)}`.")
    