from pyrogram import Client, filters
from ..Database.users import get_user
from ..Database.characters import get_anime_character
from . import YxH
from datetime import datetime
import random


@Client.on_message(filters.command("swapx"))
@YxH()  
async def swapx(client, message, user):
    # Check if it's Wednesday
    current_day = datetime.now().strftime('%A')
    if current_day != 'Wednesday':
        await message.reply("Character exchange is only allowed on Wednesdays.")
        return

    # Ensure the 'swap' field exists and 'count' is being tracked
    if not hasattr(user, 'swap') or 'count' not in user.swap:
        user.swap = {"count": 0}  # Initialize swap tracking

    # Check if user has reached the swap limit
    if user.swap['count'] >= 3:
        await message.reply("You can only exchange up to 3 characters on Wednesdays.")
        return

    # Ensure the user provided both character IDs (their own and from the database)
    try:
        user_char_id = int(message.command[1])  # The character ID from the user's collection
        db_char_id = int(message.command[2])    # The character ID from the database
    except (IndexError, ValueError):
        await message.reply("Please specify both character IDs for the swap. Example: /swapx 123 456")
        return

    # Check if the user owns the character they want to swap
    if user_char_id not in user.collection:
        await message.reply(f"You don't own the character with ID: {user_char_id}.")
        return

    # Check if the desired character exists in the database
    all_anime_character_ids = await get_anime_character_ids()
    if db_char_id not in all_anime_character_ids:
        await message.reply(f"Character with ID {db_char_id} does not exist in the database.")
        return

    # Get the details of the anime character the user wants to receive
    new_character = await get_anime_character(db_char_id)
    if not new_character:
        await message.reply(f"Character with ID {db_char_id} is not available.")
        return

    # Perform the swap
    user.collection.remove(user_char_id)  # Remove the character from the user's collection
    user.collection.append(db_char_id)    # Add the new character to the user's collection

    # Increment the swap count for the user
    user.swap['count'] += 1

    # Update the user in the database
    await user.update()

    # Notify the user of the successful swap
    await message.reply(
        f"Exchange successful! You swapped your character (ID: {user_char_id}) "
        f"for a new character (ID: {db_char_id}) - {new_character.name}."
    )