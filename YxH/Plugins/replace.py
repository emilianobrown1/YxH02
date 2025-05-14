from pyrogram import Client, filters
from ..Class.character import AnimeCharacter
from config import ANIME_CHAR_CHANNEL_ID
import requests
import os

def envs_upload(file_path) -> str:
    with open(file_path, 'rb') as file:
        return requests.post("https://envs.sh", files={"file": file}).text.strip()

@Client.on_message(filters.command("replace") & filters.reply)
@YxH(sudo=True)
async def replace_character(_, m, u):
    old_msg = m.reply_to_message
    if not old_msg or not old_msg.photo or not old_msg.caption:
        return await m.reply("Please reply to a valid character image message.")

    if old_msg.chat.id != ANIME_CHAR_CHANNEL_ID:
        return await m.reply("This message isn't from the character upload channel.")

    try:
        spl = old_msg.caption.split(";")
        name = spl[0].strip()
        anime = spl[1].strip()
        rarity = spl[2].strip()
        char_id = int(spl[3].strip())
    except Exception as e:
        return await m.reply(f"Caption format error: {e}")

    # New photo must be sent directly, then reply with /replace to the old image
    if not m.photo:
        return await m.reply("Send the new image and then reply with `/replace` to the old one.")

    status = await m.reply("Replacing image...")

    try:
        # Upload new image
        new_img = envs_upload(await m.download())

        # Remove old character entry
        await AnimeCharacter.delete(char_id)

        # Add updated character with new image
        c = AnimeCharacter(char_id, new_img, name, anime, rarity)
        await c.add()

        await status.edit(f"Character `{name}` image replaced successfully.")
    except Exception as e:
        await status.edit(f"Failed to replace image:\n{e}")