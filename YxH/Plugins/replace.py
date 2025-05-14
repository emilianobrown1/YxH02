from pyrogram import Client, filters
from . import YxH, get_anime_character
from ..Class.character import AnimeCharacter
import requests
import traceback

def envs_upload(file_path) -> str:
    with open(file_path, 'rb') as file:
        return requests.post("https://envs.sh", files={"file": file}).text.strip()

@Client.on_message(filters.command("replace") & filters.reply)
@YxH(sudo=True)
async def replace_character(_, m, u):
    # Check if the replied message is a photo
    if not m.reply_to_message or not m.reply_to_message.photo:
        return await m.reply("Please reply to the new image you want to use.")

    # Parse the ID from the command
    args = m.text.split()
    if len(args) != 2:
        return await m.reply("Usage: `/replace <character_id>`", quote=True)

    try:
        char_id = int(args[1])
    except ValueError:
        return await m.reply("Invalid character ID.", quote=True)

    # Fetch character from DB
    try:
        character = await AnimeCharacter.get(char_id)
        if not character:
            return await m.reply(f"No character found with ID `{char_id}`.")
    except Exception as e:
        return await m.reply(f"Error fetching character from DB:\n{e}")

    msg = await m.reply("Uploading new image...")

    try:
        # Upload image from the replied message
        new_image = envs_upload(await m.reply_to_message.download())

        # Delete old character
        await AnimeCharacter.delete(char_id)

        # Create new with same data but new image
        new_char = AnimeCharacter(char_id, new_image, character.name, character.anime, character.rarity)
        await new_char.add()

        await msg.edit(f"Image for `{character.name}` (ID: {char_id}) replaced successfully.")
    except Exception as e:
        await msg.edit(f"Failed:\n`{traceback.format_exc()}`")