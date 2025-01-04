import random
from pyrogram import Client, filters

# Sample powers with local image paths
powers = [
    {"name": "Power A", "image": "./images/power_a.jpg"},
    {"name": "Power B", "image": "./images/power_b.jpg"},
    {"name": "Power C", "image": "./images/power_c.jpg"},
    {"name": "Power D", "image": "./images/power_d.jpg"},
]

# User message tracking
user_message_count = {}

@Client.on_message(filters.text &  filters.private)
async def track_messages(client, message):
    user_id = message.from_user.id
    user_message_count[user_id] = user_message_count.get(user_id, 0) + 1

    if user_message_count[user_id] == 150:
        # Assign a random power
        power = random.choice(powers)
        user_message_count[user_id] = 0  # Reset message count

        # Send the power details to the user
        await message.reply_photo(
            photo=power["image"],  # Use the local file path
            caption=f"🎉 Congratulations! You've unlocked **{power['name']}**!"
        )

@Client.on_message(filters.command("power"))
async def show_powers(client, message):
    user_id = message.from_user.id
    user = await get_user(user_id)  # Retrieve user from the database

    if not user or not user.powers:
        return await message.reply("You haven't unlocked any powers yet. Keep chatting to unlock one!")

    # Fetch the first power
    first_power = user.powers[0]
    power_info = next((p for p in powers if p["name"] == first_power), None)
    
    if not power_info:
        return await message.reply("Error fetching your powers. Please try again later.")
    
    # Send the first power with a "Next" button
    await message.reply_photo(
        photo=power_info["image_path"],  # Use the local file path
        caption=f"🌟 **{power_info['name']}**\n\nDescription: {power_info.get('description', 'No description available.')}",
        reply_markup=power_navigation_markup(user_id, 0)
    )