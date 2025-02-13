from pyrogram import Client, filters
from ..Class.user import User
from . import YxH

@Client.on_message(filters.command("barracks"))
@YxH()
async def barracks(_, m, u):
    spl = m.text.split()
    if len(spl) < 2:
        return await m.reply(
            f"💡 **Usage:** `/barracks 1`\n\n"
            f"🏰 **Your Current Barracks:** `{len(u.barracks)}`\n"
            f"💎 **Each Barrack Costs:** `100 Crystals`\n"
            f"🔢 **Purchase Limit:** `1 Barrack at a time`"
        )

    try:
        count = int(spl[1])
    except ValueError:
        return await m.reply("❌ Please provide a valid number of barracks to purchase.")

    if count != 1:
        return await m.reply("❌ You can only buy 1 barrack at a time!")

    cost = 100
    if u.crystals < cost:
        return await m.reply(
            f"❌ Not enough Crystals!\n\n"
            f"You need `{cost - u.crystals}` more crystals to buy 1 barrack.\n"
            f"💎 **Your Crystals:** `{u.crystals}`\n"
            f"🏰 **Your Current Barracks:** `{len(u.barracks)}`"
        )

    # Deduct crystals and add a new barrack (store timestamp)
    u.crystals -= cost
    u.barracks.append(time.time())

    await u.update()

    await m.reply_photo(
        "Images/barrack.jpg",  # Ensure the file exists or use a URL
        caption=(
            f"🎉 **Congratulations, Commander!**\n\n"
            f"🏰 You successfully built `1` barrack 🛡️ to train your troops!\n\n"
            f"💎 **Crystals Spent:** `100`\n"
            f"🏰 **Total Barracks Now:** `{len(u.barracks)}`\n"
            f"💪 **Prepare Your Army and Lead to Glory!**"
        )
    )