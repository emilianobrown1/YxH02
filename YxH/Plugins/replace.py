from pyrogram import Client, filters
from . import YxH, get_anime_character
from ..Class.character import AnimeCharacter
import requests
import traceback

def envs_upload(file_path) -> str:
    # Uploads the image and returns its URL
    with open(file_path, 'rb') as file:
        return requests.post("https://envs.sh", files={"file": file}).text.strip()

@Client.on_message(filters.command("replace") & filters.reply)
@YxH(sudo=True)
async def replace_character(_, m, u):
    # Ensure proper command usage: /replace <character_id>
    args = m.text.split()
    if len(args) != 2:
        return await m.reply("Usage: `/replace <character_id>`", quote=True)

    try:
        char_id = int(args[1])
    except ValueError:
        return await m.reply("Invalid character ID.", quote=True)
    
    # Load existing character from the database using your helper function
    character = await get_anime_character(char_id)
    if not character:
        return await m.reply(f"No character with ID `{char_id}` found.", quote=True)
    
    # Make sure the reply message contains a new image
    if not m.reply_to_message or not m.reply_to_message.photo:
        return await m.reply("Please reply to the new image you want to use for replacement.", quote=True)
    
    status = await m.reply("Uploading new image and updating character...", quote=True)
    
    try:
        # Upload the new image
        new_image = envs_upload(await m.reply_to_message.download())
        
        # Create a new instance with the new image, while keeping the other fields the same.
        updated_char = AnimeCharacter(
            id=character.id,
            image=new_image,
            name=character.name,
            anime=character.anime,
            rarity=character.rarity,
            price=character.price
        )
        
        # The .add() method in your AnimeCharacter class uses update_one with upsert=True,
        # so it will update the document if it already exists.
        await updated_char.add()
        
        await status.edit(f"Successfully updated character `{character.name}` (ID: {character.id}) with the new image.")
    except Exception as e:
        await status.edit(f"Failed to update character image:\n{traceback.format_exc()}")