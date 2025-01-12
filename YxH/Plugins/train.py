from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# Importing necessary modules and functions
from . import YxH  # Assuming YxH is a valid decorator
from ..Database.users import get_user  # Assuming get_user function is available for database interactions
from ..Class.user import User  # Assuming User class exists and is used for user operations

# Troop Training Costs and Time
TRAINING_DETAILS = {
    "shinobi": {"cost": 1000000, "time": 5},  # 5 minutes
    "wizard": {"cost": 2000000, "time": 10},  # 10 minutes
    "sensei": {"cost": 3000000, "time": 15}   # 15 minutes
}

BARRACKS_COST = 100  # Cost of barracks

# Command to start troop training
@Client.on_message(filters.command("train"))
@YxH()  # Assuming YxH is a valid decorator
async def train_troops(_, m, u):
    user_id = m.from_user.id  # Correct variable reference (using 'm' instead of 'message')
    user = await get_user(user_id)  # Get user data from the database

    # Check if the user has a barracks
    if not user.barracks:
        # If the user doesn't have a barracks, prompt them to buy one
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Buy Barracks for 100 Crystal 🔮", callback_data="buy_barracks")]
        ])
        await m.reply("You don't have a barracks. You need one to train troops. Would you like to buy one?", reply_markup=markup)
        return

    # If the user has a barracks, allow them to proceed with troop training
    markup = troop_selection_markup()
    await m.reply("Select the troop type to train:", reply_markup=markup)

def troop_selection_markup():
    # Creating inline buttons for troop selection
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Shinobi 🥷", callback_data="shinobi")],
        [InlineKeyboardButton("Wizard 🧙", callback_data="wizard")],
        [InlineKeyboardButton("Sensei 🧝", callback_data="sensei")]
    ])

@Client.on_callback_query(filters.regex(r"shinobi|wizard|sensei"))
async def process_training_selection(client, callback_query):
    user_id = callback_query.from_user.id
    troop_type = callback_query.data
    user = await get_user(user_id)  # Fetch user data using the get_user function

    # Store the troop type for the next step
    user.active_troop_type = troop_type
    await user.update()  # Assuming the `User` class has an `update` method

    await callback_query.message.edit("How many troops would you like to train? (1 to 3)")

@Client.on_callback_query(filters.regex(r"buy_barracks"))
async def buy_barracks(client, callback_query):
    user_id = callback_query.from_user.id
    user = await get_user(user_id)  # Fetch user data

    # Check if the user has enough gold to buy a barracks
    if user.gold < BARRACKS_COST:
        await callback_query.message.edit("You don't have enough gold to buy a barracks!")
        return

    # Deduct the gold and give the user a barracks
    user.crystal -= BARRACKS_COST
    user.barracks = True  # Assuming 'barracks' is a boolean field
    await user.update()  # Update the user's data in the database

    await callback_query.message.edit("You have successfully bought a barracks! Now you can train troops.")

@Client.on_message(filters.regex(r"^[1-3]$"))
async def confirm_training(client, m):
    user_id = m.from_user.id
    user = await get_user(user_id)  # Get user data from the database

    # Retrieve the active troop type and training count
    troop_type = user.active_troop_type
    troop_count = int(m.text)

    # Check for sufficient gold
    cost_per_troop = TRAINING_DETAILS[troop_type]["cost"]
    total_cost = cost_per_troop * troop_count

    if user.gold < total_cost:
        await m.reply(f"Insufficient gold! You need {total_cost} gold.")
        return

    # Deduct gold and start training
    user.gold -= total_cost
    user.troops[troop_type] += troop_count
    await user.update()  # Update the user's data in the database

    # Start the training process (asynchronously)
    await m.reply(f"Training {troop_count} {troop_type}s started!")

    # Time to train each troop
    training_time = TRAINING_DETAILS[troop_type]["time"] * 60  # Convert to seconds

    # Notify user when training is completed
    await asyncio.sleep(training_time)
    await m.reply(f"{troop_count} {troop_type}s have finished training!")

    # Clear active troop type after training
    user.active_troop_type = None
    await user.update()  # Update the user's data after clearing active troop type