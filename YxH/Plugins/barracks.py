from pyrogram import Client, filters
from ..Class.user import User

@Client.on_message(filters.command("barracks"))
async def barracks(_, m, u):
    # Parse the count from the command
    spl = m.text.split()
    if len(spl) < 2:
        return await m.reply(
            f"💡 **Usage:** `/barracks 1`\n\n"
            f"🏰 **Your Current Barracks:** `{u.barracks if hasattr(u, 'barracks') else 0}`\n"
            f"💎 **Each Barrack Costs:** `100 Crystals`\n"
            f"🔢 **Purchase Limit:** `1 Barrack at a time`"
        )

    try:
        count = int(spl[1])  # Get the count
    except ValueError:
        return await m.reply("Please provide a valid number of barracks to purchase.")

    # Only allow purchasing 1 barrack at a time
    if count != 1:
        return await m.reply(
            f"❌ **You can only buy 1 barrack at a time!**\n\n"
            f"💡 **Usage:** `/barracks 1`"
        )

    # Cost for 1 barrack
    cost = 100

    # Ensure the `barracks` attribute exists
    if not hasattr(u, "barracks"):
        u.barracks = 0  # Initialize if not present

    # Check if the user has enough crystals
    if u.crystals < cost:
        return await m.reply(
            f"❌ **Not enough Crystals!**\n\n"
            f"You need `{cost - u.crystals}` more crystals to buy 1 barrack.\n"
            f"💎 **Your Crystals:** `{u.crystals}`\n"
            f"🏰 **Your Current Barracks:** `{u.barracks}`"
        )

    # Deduct crystals and increment barracks count
    u.crystals -= cost
    u.barracks += 1  # Safely increment the barrack count

    # Update the user in the database
    await u.update()

    # Send confirmation with an image
    caption = (
        f"🎉 **Congratulations, Commander!**\n\n"
        f"🏰 You successfully built `1` barrack 🛡️ to train your troops!\n\n"
        f"💎 **Crystals Spent:** `100`\n"
        f"🏰 **Total Barracks Now:** `{u.barracks}`\n"
        f"💪 **Prepare Your Army and Lead to Glory!**"
    )
    await m.reply_photo(
        "Images/barrack.jpg",  # Replace with the actual image path or URL
        caption=caption
    )