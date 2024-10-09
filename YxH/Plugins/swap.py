from pyrogram import Client, filters
from ..Database.users import get_user
from ..Database.characters import get_anime_character_ids
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

    # Ensure 'swap' field exists and handle missing 'count' safely
    if 'swap' not in user or 'count' not in user.swap:
        user.swap = {"count": 0}  # Initialize swap count if missing

    # Check if user has reached the swap limit
    if user.swap.get('count', 0) >= 3:
        await message.reply("You can only exchange up to 3 characters on Wednesdays.")
        return

    # Ensure the user provided a character ID to swap
    try:
        user_char_id = int(message.command[1])  # The user character ID they want to exchange
    except (IndexError, ValueError):
        await message.reply("Please specify a valid character ID from your collection. Example: /swapx 123")
        return

    # Check if the user owns the character they want to swap
    if user_char_id not in user.collection:
        await message.reply(f"You don't own the character with ID: {user_char_id}.")
        return

    # Fetch all available anime character IDs from the database
    all_anime_character_ids = await get_anime_character_ids()
    
    if not all_anime_character_ids:
        await message.reply("No anime characters are available for exchange.")
        return

    # Randomly select a new character ID from the database
    random_character_id = random.choice(all_anime_character_ids)

    # Perform the swap
    user.collection.remove(user_char_id)  # Remove the user's character
    user.collection.append(random_character_id)  # Add the new random character

    # Increment the swap count for the user
    user.swap['count'] += 1

    # Update the user in the database
    await user.update()

    # Notify the user of the successful swap
    await message.reply(
        f"Exchange successful! You swapped your character (ID: {user_char_id}) "
        f"for a new character (ID: {random_character_id})."
    )