from pyrogram import Client, filters
from . import YxH, get_anime_character
from ..Class.character import AnimeCharacter
import aiohttp
import traceback
import pickle
from ..Database import db

async def upload_to_telegraph(file_bytes: bytes, mime_type: str) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            # File type validation (updated with modern formats)
            allowed_types = {
                'image/jpeg', 'image/png', 'image/gif', 
                'image/webp', 'video/mp4', 'video/quicktime'
            }
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
                # Debugging response
                raw_response = await response.text()
                print(f"Telegraph Response: {raw_response}")  # For troubleshooting
                
                if response.status == 200:
                    result = await response.json()
                    # Correct response structure handling
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

        # Get MIME type from the photo message
        mime_type = photo_msg.photo.mime_type or 'image/jpeg'
        
        # Download image with size check
        file_bytes = await photo_msg.download(in_memory=True)
        if not file_bytes:
            return await status.edit("❌ Failed to download image")

        # Telegraph file size limit check (5MB)
        if len(file_bytes.getvalue()) > 5 * 1024 * 1024:
            return await status.edit("❌ File too large (Max 5MB allowed)")

        await status.edit("🔼 Uploading to Telegraph...")
        new_image_url = await upload_to_telegraph(
            file_bytes.getvalue(),
            mime_type=mime_type  # Fixed: Added MIME type parameter
        )

        if not new_image_url:
            return await status.edit("❌ Failed to upload image to Telegraph\nCheck logs for details")

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
        error_trace = traceback.format_exc()
        print(f"Error: {error_trace}")
        await message.reply(f"❌ Error: {str(e)}")