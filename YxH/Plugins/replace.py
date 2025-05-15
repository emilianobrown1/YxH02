from pyrogram import Client, filters
from . import YxH
from config import ANIME_CHAR_CHANNEL_ID
from ..Database.characters import get_anime_character
from ..Class.character import AnimeCharacter
import requests
import pickle
import os

def envs_upload(file_path) -> str:
    with open(file_path, 'rb') as f:
        return requests.post("https://envs.sh", files={"file": f}).text.strip()

@Client.on_message(filters.command("replace") & filters.reply)
@YxH(sudo=True)
async def replace_character_image(client, message, user):
    try:
        if len(message.command) != 2:
            return await message.reply("❗Usage: `/replace <character_id>`\n\nReply to the new image you want to set.", quote=True)

        char_id = int(message.command[1])
        photo_msg = message.reply_to_message

        if not photo_msg or not photo_msg.photo:
            return await message.reply("❗Please reply to a new image message.", quote=True)

        status = await message.reply("Fetching character info...")

        character = await get_anime_character(char_id)
        if not character:
            return await status.edit("❌ Character not found.")

        # Download and upload new image
        path = await photo_msg.download()
        new_image_url = envs_upload(path)
        os.remove(path)

        # Update character image and re-save
        character.image = new_image_url
        await db.anime_characters.update_one(
            {'id': character.id},
            {'$set': {'info': pickle.dumps(character)}}
        )

        await status.edit(f"✅ Image for `{character.name}` (ID: {character.id}) replaced successfully.")

    except Exception as e:
        await message.reply(f"❌ Error: {e}")