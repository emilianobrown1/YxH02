from pyrogram import Client, filters
import random
from ..Class.user import User
from ..universal_decorator import YxH

# Global dictionary to keep track of message counts per user.
user_message_counts = {}

# Constants for the reward trigger and cost.
MESSAGE_THRESHOLD = 100
GEMS_COST = 35000

# List of all possible powers to randomly choose from.
POWER_LIST = [
    "Darkness Shadow",
    "Frost Snow",
    "Thunder Storm",
    "Nature Ground",
    "Flame Heat Inferno",
    "Aqua Jet",
    "Strength",
    "Speed"
]

# Exclude command messages from this handler.
@Client.on_message(filters.text & filters.command)
@YxH()
async def auto_append_power(client, m, user):
    # Only process messages that come from a valid user.
    if not m.from_user:
        return

    user_id = m.from_user.id
    # Increment the user's message count.
    count = user_message_counts.get(user_id, 0) + 1
    user_message_counts[user_id] = count

    # Only proceed when the user hits the threshold.
    if count < MESSAGE_THRESHOLD:
        return

    # Reset the message count for this user.
    user_message_counts[user_id] = 0

    # Check if the user has built any barracks.
    if user.barracks_count == 0:
        await m.reply_text(
            "You haven't built any barracks yet! Build one using /barracks to start storing new powers."
        )
        return

    # Check if the user has enough gems.
    if user.gems < GEMS_COST:
        await m.reply_text(
            f"You've sent {MESSAGE_THRESHOLD} messages, but you don't have enough gems (requires {GEMS_COST}) to add a new power."
        )
        return

    # Calculate how many powers have been appended so far.
    current_power_count = sum(user.power.values())
    # Each barracks allows for 3 powers.
    max_capacity = user.barracks_count * 3

    if current_power_count >= max_capacity:
        await m.reply_text(
            f"You've reached the maximum number of appended powers ({max_capacity}) for your {user.barracks_count} barrack(s). Build more barracks to add additional powers."
        )
        return

    # Randomly select one power to append.
    selected_power = random.choice(POWER_LIST)
    # "Append" the power by increasing its count.
    user.power[selected_power] += 1

    # Deduct the gems.
    user.gems -= GEMS_COST

    # Save the updated user state to the database.
    await user.update()

    # Inform the user of the new power and their barrack status.
    await m.reply_text(
        f"🎉 Congratulations! You've sent {MESSAGE_THRESHOLD} messages.\n\n"
        f"A new power **{selected_power}** has been appended to your barracks.\n"
        f"35000 gems have been deducted.\n\n"
        f"Your barracks now hold {sum(user.power.values())}/{max_capacity} power(s)."
    )