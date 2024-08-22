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
    item = spl[0][4:]
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