from pyrogram import Client, filters
from . import YxH
from ..Class.character import AnimeCharacter
from config import ANIME_CHAR_CHANNEL_ID
import asyncio
import os

# Upload file to ANIME_CHAR_CHANNEL_ID and return the file_id
async def upload_to_telegram(client, file_path):
    msg = await client.send_photo(ANIME_CHAR_CHANNEL_ID, photo=file_path)
    return msg.photo.file_id

# Process a single message and upload its image and metadata
async def upload(client, m):
    if not m.photo or not m.caption:
        return

    if m.chat.id != ANIME_CHAR_CHANNEL_ID:
        return

    spl = m.caption.split(";")
    try:
        # Download image with a unique name
        file_path = await m.download(file_name=f"temp_{m.id}.jpg")
        file_id = await upload_to_telegram(client, file_path)
        os.remove(file_path)  # Cleanup after uploading

        # Parse caption
        name = spl[0].strip()
        anime = spl[1].strip()
        rarity = spl[2].strip()
        char_id = int(spl[3].strip())

        # Add character with file_id instead of URL
        c = AnimeCharacter(char_id, file_id, name, anime, rarity)
        await c.add()

    except Exception as e:
        raise Exception(f"Error processing message ID {m.id}\n\n{e}")

# Upload command handler
@Client.on_message(filters.command("upload"))
@YxH(sudo=True)
async def aupl(client, m, u):
    ok = await m.reply("Processing...")

    spl = m.text.split()
    if len(spl) == 3:
        start = int(spl[1])
        end = int(spl[2]) + 1
    elif len(spl) == 2:
        start = int(spl[1])
        end = start + 1
    else:
        return await m.reply("**Invalid Usage.** Use `/upload <start> <end>`")

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
        messages = await client.get_messages(ANIME_CHAR_CHANNEL_ID, batch)
        tasks = [asyncio.create_task(upload(client, msg)) for msg in messages if msg]
        await asyncio.gather(*tasks)

    await ok.edit("All characters processed successfully.")