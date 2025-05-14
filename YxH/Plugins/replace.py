from pyrogram import Client, filters
from . import YxH
from ..Class.character import AnimeCharacter
import requests

def envs_upload(file_path) -> str:
    with open(file_path, 'rb') as file:
        return requests.post("https://envs.sh", files={"file": file}).text.strip()

@Client.on_message(filters.command("replace") & filters.reply & filters.photo)
@YxH(sudo=True)
async def replace_character(_, m, u):
    args = m.text.split()
    if len(args) != 2:
        return await m.reply("Usage: `/replace <character_id>` (as a reply to new image)", quote=True)

    try:
        char_id = int(args[1])
    except:
        return await m.reply("Invalid character ID.", quote=True)

    # Get character from DB
    existing = await AnimeCharacter.get(char_id)
    if not existing:
        return await m.reply(f"No character found with ID `{char_id}`.", quote=True)

    msg = await m.reply("Uploading new image and replacing character...", quote=True)

    try:
        # Upload new image
        new_image = envs_upload(await m.download())

        # Replace entry in DB
        await AnimeCharacter.delete(char_id)
        updated = AnimeCharacter(char_id, new_image, existing.name, existing.anime, existing.rarity)
        await updated.add()

        await msg.edit(f"Image for `{existing.name}` (ID: {char_id}) replaced successfully.")
    except Exception as e:
        await msg.edit(f"Replacement failed:\n{e}")