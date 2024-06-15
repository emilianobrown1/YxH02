from pyrogram import Client, filters
from . import YxH

shields = {
    "Gold": [500000000, 24*3600],
    "Silver": [300000000, 12*3600],
    "Iron": [100000000, 8*3600]
}

@Client.on_message(filters.command("shield"))
@YxH()
async def sh(_, m, u):
    ...