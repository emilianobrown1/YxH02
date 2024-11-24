from pyrogram import Client, filters
from ..Database.users import get_user  # Import the function to fetch user data

@Client.on_message(filters.command("barracks"))
async def barracks(_, m):
    # Get the user ID
    user_id = m.from_user.id

    # Fetch user data from the database
    user_data = await get_user(user_id)
    if not user_data:
        return await m.reply("❌ **User not found in the database!** Please start the bot with /start.")
    
    # Extract crystals and barracks count
    crystals = user_data.get("crystals", 0)
    barracks = user_data.get("barracks", 0)

    # Validate the count argument (should always be 1)
    try:
        count = int(m.text.split()[1])
    except (IndexError, ValueError):
        return await m.reply(
            f"💡 **Usage:** `/barracks 1`\n\n"
            f"🏰 **Your Current Barracks:** `{barracks}`\n"
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
    if crystals < cost:
        return await m.reply(
            f"❌ **Not enough Crystals!**\n\n"
            f"You need `{cost - crystals}` more crystals to buy 1 barrack.\n"
            f"💎 **Your Crystals:** `{crystals}`\n"
            f"🏰 **Your Current Barracks:** `{barracks}`"
        )

    # Deduct crystals and update barracks
    crystals -= cost
    barracks += 1

    # Save the updated data (assuming there's a method to update user data)
    user_data["crystals"] = crystals
    user_data["barracks"] = barracks
    await save_user_data(user_id, user_data)  # Replace with the actual database save method

    # Send confirmation with an image
    caption = (
        f"🎉 **Congratulations, Commander!**\n\n"
        f"🏰 You successfully built `1` barrack 🛡️ to train your troops!\n\n"
        f"💎 **Crystals Spent:** `100`\n"
        f"🏰 **Total Barracks Now:** `{barracks}`\n"
        f"💪 **Prepare Your Army and Lead to Glory!**"
    )
    await m.reply_photo(
        "Images/barrack.jpg",  # Replace with the actual image path or URL
        caption=caption
    )
