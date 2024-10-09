from pyrogram import Client, filters
from ..Database.users import get_user
from . import YxH
from ..Database.characters import get_anime_character_ids
from datetime import datetime

@Client.on_message(filters.command("swapx"))
@YxH()
async def swapx(client, message, user):
    user = await get_user(message.from_user.id)

    # Ensure the command is only used on Wednesday
    if datetime.now().strftime("%A").lower() != "wednesday":
        return await message.reply("This command can only be used on Wednesday.")

    # Check if the user has performed 3 swaps today
    swap_count = user.swap.get("count", 0)
    if swap_count >= 3:
        return await message.reply("Maximum swaps reached for today!")

    # Parse the old and new character IDs
    try:
        from_id, to_id = map(str, message.text.split()[1:3])  # Convert to strings
    except (IndexError, ValueError):
        return await message.reply('Usage:\n\n`/swapx [old_id] [new_id]`')

    # Get all valid character IDs from the database
    all_ids = set(map(str, await get_anime_character_ids()))  # Convert to set of strings

    # Check if both character IDs are valid
    if to_id not in all_ids:
        return await message.reply("Invalid new character ID.")

    # Check if the user owns the character to be swapped
    if from_id not in user.collection:
        return await message.reply(f'You do not own the character with ID `{from_id}`!')

    # Track the user's collection
    if user.collection[from_id] == 1:
        user.collection.pop(from_id)  # Remove the character if it's the last one
    else:
        user.collection[from_id] -= 1  # Decrement the count for the character

    # Add the new character to the collection
    if to_id in user.collection:
        user.collection[to_id] += 1  # Increment the count if character already exists
    else:
        user.collection[to_id] = 1  # Add the new character with count 1

    # Increment the swap count
    user.swap["count"] = swap_count + 1

    # Update the user data in the database
    await user.update()

    await message.reply(f'Successfully swapped character ID `{from_id}` with character ID `{to_id}`!')