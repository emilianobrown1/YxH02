from pyrogram import Client, filters
from ..Database.users import get_user, db
from . import YxH
from ..Class.user import User
from ..Database.characters import get_anime_character_ids
import time

@Client.on_message(filters.command("swapx"))
async def swapx(_, m):
    user_id = m.from_user.id  # Get the user ID of the sender

    # Ensure the command is only used on Wednesday
    if time.strftime("%A").lower() != "wednesday":
        return await m.reply("This command can only be used on Wednesday.")

    # Retrieve the user's data from the database
    user_data = await get_user(user_id)
    if not user_data:
        return await m.reply("User data not found.")

    # Check if the user has performed 3 swaps today
    swap_count = user_data.get("swap", 0)
    if swapx_count >= 3:
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
    if str(from_id) not in user_data["characters"]:
        return await m.reply(f'You do not own the character with ID `{from_id}`!')

    # Perform the swap: remove the old character and add the new one
    user = User(user_id)
    await user.remove_character(from_id)
    await user.add_character(to_id)

    # Increment the swap count and update the user data in the database
    user_data["swap"] = swap_count + 1
    await user.update()  # Save the updated user data using the User class

    await m.reply(f'Successfully swapped character {from_id} with {to_id}!')