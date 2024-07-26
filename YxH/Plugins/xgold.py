from pyrogram import Client, filters
from . import YxH, get_user
import time

# Define cooldown dictionary to track last payment times
cooldown = {}

@Client.on_message(filters.command("xgold") & filters.text)
@YxH(private=False, min_old=3)
async def xgold(_, m, u):
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply("Reply to a user to share gold with.")
    
    try:
        gold = m.text.split()[1]
        if gold == "*":
            gold = u.gold
        else:
            gold = int(gold)
            
        # Minimum amount of gold to be paid
        if gold < 1:
            return await m.reply("Minimum gold amount to pay is 1.")
        
        # Maximum amount of gold to be paid
        if gold > 10000000:
            return await m.reply("You cannot pay more than 10,000,000 gold at once.")
        
        # Cooldown check
        if m.from_user.id in cooldown:
            if time.time() - cooldown[m.from_user.id] < 300:  # 300 seconds = 5 minutes
                return await m.reply("You can only pay once every 5 minutes.")
        
    except ValueError:
        return await m.reply("Usage: /xgold [gold_amount]")
    
    except IndexError:
        return await m.reply("Usage: /xgold [gold_amount]")
    
    if m.reply_to_message.from_user.id == m.from_user.id:
        return
    
    if u.gold < gold:
        return await m.reply(f"⚠️ You only have `{u.gold}` Gold.")
    
    t = await get_user(m.reply_to_message.from_user.id)
    if not t:
        return await m.reply("The replied user is not a player.")
    
    # Deduct gold from sender and add to receiver
    u.gold -= gold
    t.gold += gold
    
    # Update cooldown dictionary
    cooldown[m.from_user.id] = time.time()
    
    # Update both user's data
    await u.update()
    await t.update()
    
    await m.reply(f"**{u.user.first_name}** has paid `{gold}` Gold to **{t.user.first_name}**.")

@Client.on_message(filters.all)
async def debug_messages(client, message):
    print(f"Message received in group: {message.text}")