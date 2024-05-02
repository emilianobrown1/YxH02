from pyrogram import Client, filters
from . import YxH, get_date, get_week
from ..Utils.templates import xprofile_template
from ..Utils.markups import
from  bonus 
import  xprofile_markup
import random


@Client.on_message(filters.command("mine") & filters.group)
@YxH()
async def mine(_, m, user):
    
    min_gold_required = 500
    
    
    if user.gold < min_gold_required:
        return await m.reply("You need at least 500 gold to start mining.")
    
    
    success = random.randint(0, 100) < 20  
    if success:
        
        user.gold_mines += 1  
        await m.reply("You've struck gold! Reward: Gold Mine")
    else:
        
        await m.reply("No luck this time, keep mining!")
    
    # Update the user's data
    return await user.update()
