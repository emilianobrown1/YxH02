from pyrogram import Client, filters
from ..Database.users import get_user
from ..universal_decorator import YxH
import random

@Client.on_message(filters.command("getpower"))
@YxH()
async def acquire_power(client, message, user):
    # Configuration
    REQUIRED_MESSAGES = 250
    POWER_COST = 35000
    MAX_PER_BARRACK = 3
    
    # Check message requirement
    if user.messages_for_power < REQUIRED_MESSAGES:
        needed = REQUIRED_MESSAGES - user.messages_for_power
        await message.reply(
            f"📭 Need {needed} more messages!\n"
            f"Progress: {user.messages_for_power}/{REQUIRED_MESSAGES}"
        )
        return

    # Check gem balance
    if user.gems < POWER_COST:
        await message.reply(
            f"💎 Insufficient gems!\n"
            f"Required: {POWER_COST:,}\n"
            f"Your balance: {user.gems:,}"
        )
        return

    # Calculate power capacity
    max_powers = user.barracks_count * MAX_PER_BARRACK
    current_powers = sum(user.power.values())
    
    if current_powers >= max_powers:
        await message.reply(
            f"🚧 Maximum capacity reached!\n"
            f"Powers: {current_powers}/{max_powers}\n"
            "Build more barracks with /barracks"
        )
        return

    # Select random available power
    power_options = [power for power, count in user.power.items() if count < MAX_PER_BARRACK]
    if not power_options:
        await message.reply("🎉 All powers at maximum capacity!")
        return

    selected_power = random.choice(power_options)
    
    # Update user data
    user.gems -= POWER_COST
    user.power[selected_power] += 1
    user.messages_for_power = 0  # Reset counter
    await user.update()

    # Send success message
    await message.reply(
        f"⚡ **Power Acquired!**\n\n"
        f"✨ {selected_power}\n"
        f"🏰 Total Powers: {current_powers + 1}/{max_powers}\n"
        f"💎 Cost: {POWER_COST:,} gems\n"
        f"📬 Messages used: {REQUIRED_MESSAGES}"
    )
