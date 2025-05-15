from pyrogram import Client, filters
from . import YxH, get_anime_character
from config import ANIME_CHAR_CHANNEL_ID
from ..Database import db
from ..Class.character import AnimeCharacter
import requests
import pickle
import os

# Upload function
def envs_upload(file_path) -> str:
    with open(file_path, 'rb') as file:
        return requests.post("https://envs.sh", files={"file": file}).text.strip()

# Replace command
@Client.on_message(filters.command("replace") & filters.reply)
@YxH(sudo=True)
async def replace_character_image(client, message, user):
    if len(message.command) != 2:
        return await message.reply("❗Usage: `/replace <character_id>`\n(Reply to new image to update)")

    try:
        char_id = int(message.command[1])
    except ValueError:
        return await message.reply("❗ Character ID must be a number.")

    reply_msg = message.reply_to_message
    if not reply_msg or not reply_msg.photo:
        return await message.reply("❗You must reply to the new image.")

    status = await message.reply("⏳ Processing replacement...")

    character = await get_anime_character(char_id)
    if not character:
        return await status.edit("❌ Character not found.")

    try:
        # Upload new image with unique filename
        photo_path = await reply_msg.download(file_name=f"replace_temp_{message.id}.jpg")
        new_image_url = envs_upload(photo_path)
        os.remove(photo_path)

        # Delete old character from DB
        await db.anime_characters.delete_one({"id": char_id})

        # Recreate character with updated image
        updated = AnimeCharacter(
            id=character.id,
            image=new_image_url,
            name=character.name,
            anime=character.anime,
            rarity=character.rarity,
            price=character.price
        )
        await updated.add()

        await status.edit(f"✅ `{character.name}` image updated successfully.")
    except Exception as e:
        await status.edit(f"❌ Failed to update:\n`{e}`")