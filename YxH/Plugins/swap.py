from pyrogram import Client, filters
from ..Database.users import get_user, update_dic
from ..Class.user import User
from ..Database.characters import get_anime_character_ids
import time
import random

@Client.on_message(filters.command("swapx"))
async def swapx(client, m):
    user_id = m.from_user.id  # Assuming the user ID is the sender's ID
    
    # Check if the command is used on Wednesday
    if time.strftime("%A").lower() != "wednesday":
        return await m.reply("This command can only be used on Wednesday.")
    
    # Retrieve the user's data
    dic = await get_user(user_id)
    str_user_id = str(user_id)
    
    # Check if the user has already performed 3 swaps
    done = dic.get(str_user_id, 0)
    if done >= 3:
        return await m.reply('Maximum swaps reached for today!')
    
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
    
    # Check if the user owns the old character
    user_data = await get_user(user_id)
    if str(from_id) not in user_data["characters"]:
        return await m.reply(f'You do not have a character with ID `{from_id}`!')
    
    # Perform the swap: remove the old character and add the new one
    user = User(user_id)
    await user.remove_character(from_id)
    await user.add_character(to_id)
    
    # Update the swap counter and store the updated data
    dic[str_user_id] = done + 1
    await update_dic(dic)
    
    await m.reply(f'Successfully swapped character `{from_id}` with `{to_id}`!')
