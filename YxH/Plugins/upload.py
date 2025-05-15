from pyrogram import Client, filters
from . import YxH
from ..Class.character import AnimeCharacter
from config import ANIME_CHAR_CHANNEL_ID
import asyncio
import os
import cloudinary.uploader
import cloudinary.api

# Cloudinary credentials
cloudinary.config(
    cloud_name="dlew93drg",
    api_key="526717458836789",
    api_secret="SnQHHN1dc4sWYO_lrrwHHMul140"
)

# Upload image to Cloudinary
def upload_to_cloudinary(file_path):
    result = cloudinary.uploader.upload(file_path)
    return result["secure_url"]

# Process a single message
async def upload(m):
    if not m.photo or not m.caption:
        return
    if m.chat.id != ANIME_CHAR_CHANNEL_ID:
        return

    try:
        # Download image locally
        file_path = await m.download(file_name=f"temp_{m.id}.jpg")
        # Upload to Cloudinary
        image_url = upload_to_cloudinary(file_path)
        os.remove(file_path)

        # Parse caption
        name, anime, rarity, char_id = [x.strip() for x in m.caption.split(";")]
        char_id = int(char_id)

        # Save character to DB
        c = AnimeCharacter(char_id, image_url, name, anime, rarity)
        await c.add()

    except Exception as e:
        raise Exception(f"Error at message ID {m.id}\n\n{e}")

# /upload command handler
@Client.on_message(filters.command("upload"))
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
        return await m.reply("**Invalid Usage.** Use `/upload <start> <end>`")

    # Create batches of 200 max
    batches = []
    while end - st > 200:
        batches.append(list(range(st, st + 200)))
        st += 200
    if end - st > 0:
        batches.append(list(range(st, end)))

    for i, batch in enumerate(batches):
        await ok.edit(f"Processing batch {i + 1}/{len(batches)}...")
        messages = await _.get_messages(ANIME_CHAR_CHANNEL_ID, batch)
        tasks = [asyncio.create_task(upload(msg)) for msg in messages if msg]
        await asyncio.gather(*tasks)

    await ok.edit("All characters uploaded successfully.")