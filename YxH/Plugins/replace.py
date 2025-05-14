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
        # Get character ID from the command: /replace <id>
        _, char_id = m.text.strip().split()
        char_id = int(char_id)
    except:
        return await m.reply("❌ Usage: `/replace <character_id>`\n\n(Reply to the new image)")

    # Fetch character from DB
    char = await get_anime_character(char_id)
    if not char:
        return await m.reply("❌ Character not found in database.")

    status = await m.reply("⏳ Uploading new image...")

    try:
        # Upload new image to envs.sh
        downloaded = await reply.download()
        new_image = envs_upload(downloaded)
        os.remove(downloaded)

        # Update character image manually
        char.image = new_image

        # Re-save with updated image
        await db.anime_characters.update_one(
            {'id': char_id},
            {'$set': {'info': pickle.dumps(char)}}
        )

        # Update local cache
        chars[char_id] = char

        await status.edit(f"✅ Character `{char.name}` (ID: `{char.id}`) image replaced successfully.")
    except Exception as e:
        await status.edit(f"❌ Failed to replace image:\n`{e}`")