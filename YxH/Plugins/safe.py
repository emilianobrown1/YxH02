from . import YxH
from pyrogram import Client, filters

@Client.on_message(filters.command(["safexgd", "safexgm", "safexc"]))
@YxH(private=False)
async def safe(_, m, u):
    if not u.treasure_state:
        return await m.reply("Unlock Treasure First to save.")
    spl = m.text.split()
    try:
        inp = int(spl[1])
    except:
        return await m.reply("Enter the amount to be transferred.")
    item = spl[0][6:]
    if item == "gd":
        if u.gold < inp:
            return await m.reply(f"You only having `{inp}` gold.")
        u.gold -= inp
        u.treasure[0] += inp
        await u.update()
        return await m.reply(f"`{inp}` gold has been moved to treasure.")
    elif item == "gm":
        if u.gems < inp:
            return await m.reply(f"You only having `{inp}` gems.")
        u.gems -= inp
        u.treasure[1] += inp
        await u.update()
        return await m.reply(f"`{inp}` gems has been moved to treasure.")
    elif item == "c":
        if u.crystals < inp:
            return await m.reply(f"You only having `{inp}` crystals.")
        u.crystals -= inp
        u.treasure[2] += inp
        await u.update()
        return await m.reply(f"`{inp}` crystals has been moved to treasure.")

@Client.on_message(filters.command(["rsafexgd", "rsafexgm", "rsafexc"]))
@YxH(private=False)
async def rsafe(_, m, u):
    if not u.treasure_state:
        return await m.reply("Unlock Treasure First to withdraw.")
    
    spl = m.text.split()
    
    # Determine the item based on the command used
    item = spl[0][8:]  # Extract 'gd', 'gm', or 'c' from the command name
    
    if item not in ["gd", "gm", "c"]:
        return await m.reply("Invalid item. Use `rsafexgd`, `rsafexgm`, or `rsafexc`.")
    
    if len(spl) < 2:
        return await m.reply("Enter the amount to be transferred.")
    
    try:
        inp = int(spl[1])
    except ValueError:
        return await m.reply("Please enter a valid number for the amount.")
    
    # Handle the withdrawal based on the item type
    if item == "gd":
        if u.treasure[0] < inp:
            return await m.reply(f"You only have `{u.treasure[0]}` gold in the treasure.")
        u.treasure[0] -= inp
        u.gold += inp
        await u.update()
        return await m.reply(f"`{inp}` gold has been removed from treasure.")
    
    elif item == "gm":
        if u.treasure[1] < inp:
            return await m.reply(f"You only have `{u.treasure[1]}` gems in the treasure.")
        u.treasure[1] -= inp
        u.gems += inp
        await u.update()
        return await m.reply(f"`{inp}` gems have been removed from treasure.")
    
    elif item == "c":
        if u.treasure[2] < inp:
            return await m.reply(f"You only have `{u.treasure[2]}` crystals in the treasure.")
        u.treasure[2] -= inp
        u.crystals += inp
        await u.update()
        return await m.reply(f"`{inp}` crystals have been removed from treasure.")