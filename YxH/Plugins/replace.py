from pyrogram import Client, filters
from . import YxH
from ..Class.character import AnimeCharacter
import requests

def envs_upload(file_path) -> str:
    with open(file_path, 'rb') as file:
        return requests.post("https://envs.sh", files={"file": file}).text.strip()

@Client.on_message(filters.command("replace") & filters.reply)
@YxH(sudo=True)
async def replace_character(_, m, u):
    old_msg = m.reply_to_message
    if not old_msg or not old_msg.caption or not old_msg.photo:
        return await m.reply("Please reply to a valid character image message with caption.")

    try:
        spl = old_msg.caption.split(";")
        name = spl[0].strip()
        anime = spl[1].strip()
        rarity = spl[2].strip()
        char_id = int(spl[3].strip())
    except Exception as e:
        return await m.reply(f"Caption format error: {e}")

    if not m.photo:
        return await m.reply("Send the new image and then reply to the old one with `/replace`.")

    status = await m.reply("Replacing image in database...")

    try:
        # Upload new image
        new_img = envs_upload(await m.download())

        # Replace character in database
        await AnimeCharacter.delete(char_id)
        c = AnimeCharacter(char_id, new_img, name, anime, rarity)
        await c.add()

        await status.edit(f"Character `{name}` image replaced successfully in the database.")
    except Exception as e:
        await status.edit(f"Failed to replace character image:\n{e}")