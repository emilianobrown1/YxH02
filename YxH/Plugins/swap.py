from pyrogram import Client, filters
from ..Database.users import get_user
from . import YxH
from ..Database.characters import get_anime_character_ids
import time

@Client.on_message(filters.command("swapx"))
async def swapx(_, m, u):
    user_id = u.user.id  # Get the user ID from the User instance

    # Ensure the command is only used on Wednesday
    if time.strftime("%A").lower() != "wednesday":
        return await m.reply("This command can only be used on Wednesday.")

    # Check if the user has performed 3 swaps today
    swap_count = u.swap.get("count", 0)  # Accessing the swap attribute from the User instance
    if swap_count >= 3:
        return await m.reply("Maximum swaps reached for today!")

    # Parse the old and new character IDs
    try:
        from_id = int(m.text.split()[1])
        to_id = int(m.text.split()[2])
    except (IndexError, ValueError):
        return await m.reply('Usage:\n\n`/swapx [old_id] [new_id]`')

    # Check if the new character ID is valid
    total_characters = await get_anime_character_ids()
    if to_id > total_characters:
        return await m.reply("Invalid new character ID.")

    # Verify if the user owns the character to be swapped
    if str(from_id) not in u.collection:  # Ensure u.collection holds the character IDs
        return await m.reply(f'You do not own the character with ID `{from_id}`!')

    # Remove the old character from the user's collection
    u.collection.remove(str(from_id))  # Assuming collection is a list; otherwise use `del u.collection[str(from_id)]`

    # Add the new character to the user's collection
    u.collection.append(str(to_id))  # Adding the new character ID

    # Increment the swap count and update the user data in the database
    u.swap["count"] = swap_count + 1
    await u.update()  # Save the updated user data using the User class

    await m.reply(f'Successfully swapped character {from_id} with {to_id}!')