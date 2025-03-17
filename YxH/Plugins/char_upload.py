from pyrogram import Client, filters
from . import YxH
from ..Class.character import AnimeCharacter, YaoiYuriCharacter
from config import ANIME_CHAR_CHANNEL_ID
import asyncio
import os
import requests

def envs_upload(file_path) -> str:
    with open(file_path, 'rb') as file:
        return requests.post("https://envs.sh", files={"file": file}).text.strip()

async def upload(m):
    # m = await cli.get_messages(ANIME_CHAR_CHANNEL_ID, msg_id)
    if not m.photo or not m.caption:
        return

    if m.chat.id != ANIME_CHAR_CHANNEL_ID:
        return
    spl = m.caption.split(";")
    try:
        image = envs_upload(await m.download())
        name = spl[0].strip()
        anime = spl[1].strip()
        rarity = spl[2].strip()
        id = int(spl[3].strip())
    except Exception as e:
        raise Exception(f"Error at {m.id}\n\n{e}")
    c = AnimeCharacter(id, image, name, anime, rarity)
    await c.add()

@Client.on_message(filters.command("aupl"))
@YxH(sudo=True)
async def aupl(_, m, u):
    ok = await m.reply("Processing...")
    spl = m.text.split()
    if len(spl) == 3:
        st = int(spl[1])
        end = int(spl[2]) + 1
    elif len(spl) == 2:
        st = int(spl[1])
        end = st + 1
    else:
        return await m.reply("**Invalid Usage.**")
    batches = []
    while end - st > 200:
        batches.append(list(range(st, st+200)))
        st += 200
    if end - st != 0:
        batches.append(list(range(st, end)))
    for x in batches:
        await ok.edit(f"Processing batch: {batches.index(x)}/{len(batches)}.")
        messages = await _.get_messages(ANIME_CHAR_CHANNEL_ID, x)
        tasks = []
        for i in messages:
            tasks.append(asyncio.create_task(upload(i)))
        await asyncio.gather(*tasks)
    await ok.edit("Processed.")
