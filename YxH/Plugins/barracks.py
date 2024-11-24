from pyrogram import Client, filters
from . import YxH
from ..Class import User

@Client.on_message(filters.command("barracks"))
async def barracks(_, m):
    # Initialize user instance from User class
    user_id = m.from_user.id
    u = User(user_id)

    # Ensure the user is loaded correctly
    if u is None:
        return await m.reply("❌ **User not found in the database!** Please start the bot with /start.")

    # Validate the count argument (should always be 1)
    try:
        count = int(m.text.split()[1])
    except (IndexError, ValueError):
        return await m.reply(
            f"💡 **Usage:** `/barracks 1`\n\n"
            f"🏰 **Your Current Barracks:** `{u.barracks}`\n"
            f"💎 **Each Barrack Costs:** `100 Crystals`\n"
            f"🔢 **Purchase Limit:** `1 Barrack at a time`"
        )

    # Allow only 1 barrack per purchase
    if count != 1:
        return await m.reply(
            f"❌ **You can only buy 1 barrack at a time!**\n\n"
            f"💡 **Usage:** `/barracks 1`"
        )

    # Cost for 1 barrack
    cost = 100

    # Check if the user has enough crystals
    if int(u.crystals) < cost:
        return await m.reply(
            f"❌ **Not enough Crystals!**\n\n"
            f"You need `{cost - u.crystals}` more crystals to buy 1 barrack.\n"
            f"💎 **Your Crystals:** `{u.crystals}`\n"
            f"🏰 **Your Current Barracks:** `{u.barracks}`"
        )

    # Deduct crystals and update barracks
    u.crystals -= cost
    u.barracks += 1
    u.update()  # Save changes to the user instance

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
