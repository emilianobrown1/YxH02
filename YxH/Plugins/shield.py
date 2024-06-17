from pyrogram import Client, filters
from . import YxH, grt
import time

shields = {
    "Gold": [500000000, 24*3600],
    "Silver": [300000000, 12*3600],
    "Iron": [100000000, 8*3600]
}

@Client.on_message(filters.command("shield"))
@YxH()
async def sh(_, m, u):
    if t.shield:
        if int(time.time()-t.shield[1]) > t.shield[0]:
            t.shield = []
    if t.shield:
        left = t.shield[0] - int(time.time()-t.shield[1])
        return await m.reply("**You already having a shield equipped and will be expired after `{grt(left)}`.")