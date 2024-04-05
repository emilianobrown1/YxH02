from pyrogram import Client, filters
from . import YxH
from ..Class.character import AnimeCharacter, YaoiYuriCharacter
from config import ANIME_CHAR_CHANNEL_ID
import asyncio

async def upload(cli: Client, msg_id: int):
    m = await cli.get_messages(ANIME_CHAR_CHANNEL_ID, msg_id)
    if not m.photo or not m.caption:
        raise Exception("Invalid")
    spl = m.caption.split(";")
    try:
        name = spl[0].strip()
        anime = spl[1].strip()
        rarity = spl[2].strip()
        id = int(spl[3].strip())
    except:
        raise Exception(f"Error at {msg_id}")
    c = AnimeCharacter(id, name, anime, rarity)
    await c.add()

@Client.on_message(filters.command("aupl"))
@YxH(sudo=True)
async def aupl(_, m, u):
    spl = m.text.split()
    start = int(spl[1])
    end = int(spl[2]) + 1
    tasks = []
    for i in range(start, end):
        tasks.append(asyncio.create_task(upload(_, i)))
    await asyncio.gather(*tasks)