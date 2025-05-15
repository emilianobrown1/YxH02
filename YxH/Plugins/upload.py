from pyrogram import Client, filters
from . import YxH
from ..Class.character import AnimeCharacter, YaoiYuriCharacter
from config import ANIME_CHAR_CHANNEL_ID
import asyncio
import os
import requests

# Upload file to envs.sh and return the link
def envs_upload(file_path) -> str:
    with open(file_path, 'rb') as file:
        return requests.post("https://envs.sh", files={"file": file}).text.strip()

# Process a single message and upload its image and metadata
async def upload(m):
    if not m.photo or not m.caption:
        return

    if m.chat.id != ANIME_CHAR_CHANNEL_ID:
        return

    spl = m.caption.split(";")
    try:
        # Download image with a unique name
        file_path = await m.download(file_name=f"temp_{m.id}.jpg")
        image = envs_upload(file_path)
        os.remove(file_path)  # Cleanup after uploading

        # Parse caption
        name = spl[0].strip()
        anime = spl[1].strip()
        rarity = spl[2].strip()
        char_id = int(spl[3].strip())

        # Add character
        c = AnimeCharacter(char_id, image, name, anime, rarity)
        await c.add()

    except Exception as e:
        raise Exception(f"Error processing message ID {m.id}\n\n{e}")

# Upload command handler
@Client.on_message(filters.command("upload"))
@YxH(sudo=True)
async def aupl(_, m, u):
    ok = await m.reply("Processing...")

    spl = m.text.split()
    if len(spl) == 3:
        start = int(spl[1])
        end = int(spl[2]) + 1
    elif len(spl) == 2:
        start = int(spl[1])
        end = start + 1
    else:
        return await m.reply("**Invalid Usage.** Use `/aupl <start> <end>`")

    # Batch in chunks of 200
    batches = []
    while end - start > 200:
        batches.append(list(range(start, start + 200)))
        start += 200
    if end - start > 0:
        batches.append(list(range(start, end)))

    # Process batches
    for i, batch in enumerate(batches):
        await ok.edit(f"Processing batch {i + 1}/{len(batches)}...")
        messages = await _.get_messages(ANIME_CHAR_CHANNEL_ID, batch)
        tasks = [asyncio.create_task(upload(msg)) for msg in messages if msg]
        await asyncio.gather(*tasks)

    await ok.edit("All characters processed successfully.")