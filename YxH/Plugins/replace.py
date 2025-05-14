from pyrogram import Client, filters
from . import YxH, get_anime_character
from ..Class.character import AnimeCharacter
import requests
import traceback
import requests
import pickle
import os
from ..Database import db

def envs_upload(file_path) -> str:
    with open(file_path, 'rb') as file:
        return requests.post("https://envs.sh", files={"file": file}).text.strip()

@Client.on_message(filters.command("replace") & filters.reply)
@YxH(sudo=True)
async def replace_character(_, m, u):
    reply = m.reply_to_message

    if not reply or not reply.photo:
        return await m.reply("❌ Please reply to the **new image**.")

    try:
        # /replace <character_id>
        _, char_id = m.text.strip().split()
        char_id = int(char_id)
    except:
        return await m.reply("❌ Usage: `/replace <character_id>` (reply to the new image)")

    status = await m.reply("⏳ Fetching character...")

    try:
        char = await get_anime_character(char_id)
        if not char:
            return await status.edit("❌ Character not found in database.")

        # Upload new image
        file = await reply.download()
        new_image_url = envs_upload(file)
        os.remove(file)

        # Update only the image
        char.image = new_image_url

        # Save updated character back
        await db.anime_characters.update_one(
            {'id': char_id},
            {'$set': {'info': pickle.dumps(char)}}
        )

        await status.edit(f"✅ Updated image for `{char.name}` (ID: `{char.id}`) successfully.")
    except Exception as e:
        await status.edit(f"❌ Failed to replace image:\n`{e}`")