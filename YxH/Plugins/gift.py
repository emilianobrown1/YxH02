from pyrogram import Client, filters
from . import YxH, get_date

@Client.on_message(filters.command("xgift"))
@YxH()
async def xgift(_, m, u):
    ...