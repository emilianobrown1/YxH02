from pyrogram import Client, filters
from ..Database.users import get_user
from ..Database.characters import get_anime_character_ids, get_anime_character
from . import YxH
from datetime import datetime
import random


@Client.on_message(filters.command("swapx"))
@YxH()  
async def swapx(client, message, user):
    # Check if it's Sunday
    current_day = datetime.now().strftime('%A')
    if current_day != 'Sunday':
        await message.reply("Character exchange is only allowed on Sunday.")
        return

    # Initialize the 'swap' field if not present
    if not hasattr(user, 'swap'):
        user.swap = {"count": 0, "last_swap_date": None}

    # Check if the last swap was on a different Sunday, if so reset the swap count
    last_swap_date = user.swap.get('last_swap_date')
    today_date = datetime.now().date()

    if last_swap_date is None or last_swap_date != today_date:
        user.swap['count'] = 0  # Reset count on a new Sunday
        user.swap['last_swap_date'] = today_date  # Update last swap date

    # Check if user has reached the swap limit
    if user.swap['count'] >= 3:
        await message.reply("You can only exchange up to 3 characters on Sunday.")
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
    all_anime_character_ids = await get_anime_character_ids()  # Get all character IDs from the database
    if db_char_id not in all_anime_character_ids:
        await message.reply(f"Character with ID {db_char_id} does not exist in the database.")
        return

    # Get the details of the anime character the user wants to receive
    new_character = await get_anime_character(db_char_id)
    if not new_character:
        await message.reply(f"Character with ID {db_char_id} is not available.")
        return

    # Perform the swap (removing only one instance of the character)
    if isinstance(user.collection, list):
        try:
            user.collection.remove(user_char_id)  # Remove only one instance of the character
        except ValueError:
            await message.reply(f"An error occurred while removing the character with ID: {user_char_id}.")
            return
    elif isinstance(user.collection, dict):
        # If using a dictionary with count system, decrease the count or remove the key if count is 1
        if user.collection.get(user_char_id, 0) > 1:
            user.collection[user_char_id] -= 1  # Decrease count if more than one instance exists
        else:
            del user.collection[user_char_id]  # Remove the key if only one instance exists

    # Add the new character to the user's collection
    if isinstance(user.collection, list):
        user.collection.append(db_char_id)  # Add new character to the collection
    elif isinstance(user.collection, dict):
        user.collection[db_char_id] = user.collection.get(db_char_id, 0) + 1  # Increment count or add new

    # Increment the swap count for the user
    user.swap['count'] += 1

    # Update the user in the database
    await user.update()

    # Notify the user of the successful swap
    await message.reply(
        f"Swap successful! You swapped your character (ID: {user_char_id}) "
        f"for a new character (ID: {db_char_id}) - {new_character.name}."
    )