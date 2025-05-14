from pyrogram import Client, filters
from . import YxH, get_anime_character
from ..Class.character import AnimeCharacter
import aiohttp
import traceback
import pickle
from ..Database import db

def detect_mime_type(file_bytes: bytes) -> str:
    """Detect MIME type from file bytes"""
    # Check common image signatures
    if file_bytes.startswith(b'\xFF\xD8\xFF'):
        return 'image/jpeg'
    elif file_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    elif file_bytes[0:3] == b'GIF':
        return 'image/gif'
    elif file_bytes.startswith(b'RIFF') and file_bytes[8:12] == b'WEBP':
        return 'image/webp'
    # Add more formats as needed
    return 'image/jpeg'  # Default fallback

async def upload_to_telegraph(file_bytes: bytes, mime_type: str) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            # File type validation
            allowed_types = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
            if mime_type not in allowed_types:
                raise ValueError(f"Unsupported MIME type: {mime_type}")

            # Generate filename with valid extension
            ext = mime_type.split('/')[-1]
            form_data = aiohttp.FormData()
            form_data.add_field('file', file_bytes, 
                              filename=f'media.{ext}', 
                              content_type=mime_type)

            async with session.post(
                "https://telegra.ph/upload",
                data=form_data,
                timeout=30
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return f"https://telegra.ph{result[0].get('src', '')}"
                return None

        except Exception as e:
            print(f"Upload failed: {traceback.format_exc()}")
            return None

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

        status = await message.reply("🔄 Fetching character info...")

        character = await get_anime_character(char_id)
        if not character:
            return await status.edit("❌ Character not found.")

        # Download image directly to memory
        file_bytes = await photo_msg.download(in_memory=True)
        if not file_bytes:
            return await status.edit("❌ Failed to download image")

        # Detect MIME type from file content
        file_content = file_bytes.getvalue()
        mime_type = detect_mime_type(file_content)

        await status.edit("🔼 Uploading to Telegraph...")
        new_image_url = await upload_to_telegraph(file_content, mime_type)

        if not new_image_url:
            return await status.edit("❌ Failed to upload image to Telegraph")

        # Update character image and re-save
        character.image = new_image_url
        await db.anime_characters.update_one(
            {'id': character.id},
            {'$set': {'info': pickle.dumps(character)}}
        )

        await status.edit(f"✅ Image for `{character.name}` (ID: {character.id}) replaced successfully.\n\nNew URL: {new_image_url}")

    except ValueError:
        await message.reply("❗Invalid character ID format")
    except Exception as e:
        error