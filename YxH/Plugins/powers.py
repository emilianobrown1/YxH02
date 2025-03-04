from pyrogram import Client, filters
import random
from ..Class.user import User
from ..universal_decorator import YxH

# Constants for the reward trigger and cost
MESSAGE_THRESHOLD = 100
GEMS_COST = 35000
MAX_POWER_LEVEL = 3

@Client.on_message(filters.text & ~filters.command)
@YxH()
async def auto_append_power(client, m, user):
    # Only process messages from valid users
    if not m.from_user or m.from_user.is_bot:
        return

    # Update message count in database
    user.message_count += 1
    processed_batches = 0

    # Process all eligible message batches
    while (user.message_count >= MESSAGE_THRESHOLD and 
           user.gems >= GEMS_COST and 
           user.barracks_count > 0):
        # Calculate capacity before processing
        current_powers = sum(user.power.values())
        max_capacity = user.barracks_count * MAX_POWER_LEVEL

        if current_powers >= max_capacity:
            await m.reply_text(
                f"⛔ Maximum power capacity reached ({max_capacity})! "
                "Build more barracks with /barracks"
            )
            break

        # Find available powers that can be upgraded
        available_powers = [
            power for power, level in user.power.items()
            if level < MAX_POWER_LEVEL
        ]

        if not available_powers:
            await m.reply_text(
                "✨ All powers have reached maximum level! "
                "No more upgrades possible."
            )
            break

        # Deduct messages and gems
        user.message_count -= MESSAGE_THRESHOLD
        user.gems -= GEMS_COST
        processed_batches += 1

        # Select and upgrade power
        selected_power = random.choice(available_powers)
        user.power[selected_power] += 1

        # Update database after each batch
        await user.update()

    # Send final notification if any batches processed
    if processed_batches > 0:
        current_powers = sum(user.power.values())
        max_capacity = user.barracks_count * MAX_POWER_LEVEL
        
        await m.reply_text(
            f"⚡ **Power Upgrade Complete!**\n\n"
            f"📨 Processed {processed_batches} batch(es) of {MESSAGE_THRESHOLD} messages\n"
            f"💎 Deducted {GEMS_COST * processed_batches} gems\n"
            f"✨ New power level: {selected_power} ({user.power[selected_power]}/{MAX_POWER_LEVEL})\n"
            f"🏰 Total powers: {current_powers}/{max_capacity}"
        )
    else:
        # Update message count even if no batches processed
        await user.update()