from pyrogram import Client, filters
from . import YxH, get_date, get_week
import random

@Client.on_message(filters.command("mine"))
@YxH()
async def mine(_, m, user):
    # Minimum gold required to mine
    min_gold_required = 500
    
    
    if user.gold < min_gold_required:
        return await m.reply("You need at least 500 gold to start mining.")
    
    
    success = random.randint(0, 100) < 20  
    if success:
        # If successful, add a gold mine to the user's inventory or increase their gold count
        user.gold_mines += 1  # Assuming 'gold_mines' is an attribute of the user object
        await m.reply("You've struck gold! Reward: Gold Mine")
    else:
        # If not successful, encourage the user to try again
        await m.reply("No luck this time, keep mining!")
    
    # Update the user's data
    return await user.update()
