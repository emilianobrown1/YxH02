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
    EMOJI_MAP = {
        "Darkness Shadow": "🌑",
        "Frost Snow": "❄️",
        "Thunder Storm": "⚡",
        "Nature Ground": "🌿",
        "Flame Heat Inferno": "🔥",
        "Aqua Jet": "💧",
        "Strength": "💪",
        "Speed": "⚡"
    }

    # Check message requirement first
    if user.messages_for_power < REQUIRED_MESSAGES:
        needed = REQUIRED_MESSAGES - user.messages_for_power
        return await message.reply(
            f"**🔥 Power Acquisition Requirements 🔥**\n\n"
            f"📩 Messages Needed: `{needed}` more\n"
            f"📊 Your Progress: `{user.messages_for_power}/250`\n"
            f"💎 Gem Requirement: `35,000`\n\n"
            "_Send more messages in this chat to qualify!_"
        )

    # Check gem balance
    if user.gems < POWER_COST:
        return await message.reply(
            f"💎 **Insufficient Gems!**\n\n"
            f"Required: `{POWER_COST:,}`\n"
            f"Your Balance: `{user.gems:,}`\n\n"
            "_Earn gems through battles and events!_"
        )

    # Calculate capacity
    max_powers = user.barracks_count * MAX_PER_BARRACK
    current_power = sum(user.power.values())

    if current_power >= max_powers:
        return await message.reply(
            f"🏰 **Maximum Capacity Reached!**\n\n"
            f"Total Powers: `{current_power}/{max_powers}`\n"
            "Upgrade your barracks using:\n`/barracks`"
        )

    # Get available powers
    power_options = [
        (power, count) for power, count in user.power.items() 
        if count < MAX_PER_BARRACK
    ]

    if not power_options:
        return await message.reply("🎉 **All powers at maximum level!**")

    # Select random power
    selected_power, current_level = random.choice(power_options)
    emoji = EMOJI_MAP.get(selected_power, "✨")

    # Update user data
    user.gems -= POWER_COST
    user.power[selected_power] += 1
    user.messages_for_power = 0
    await user.update()

    # Send success message
    await message.reply(
        f"{emoji} **POWER ACQUIRED!** {emoji}\n\n"
        f"• **Type:** `{selected_power}`\n"
        f"• **Level:** `{current_level + 1}`\n"
        f"• **Total Powers:** `{current_power + 1}/{max_powers}`\n\n"
        f"__Resources Spent:__\n"
        f"💎 Gems: `{POWER_COST:,}`\n"
        f"📩 Messages: `250`"
    )


@Client.on_message(filters.all & filters.command("getpower"))  # Added message handler
async def track_activity(client, message):
    """Track messages for power acquisition"""
    if not message.from_user:
        return

    user = await get_user(message.from_user)
    user.messages_for_power += 1  # Increment counter
    await user.update()