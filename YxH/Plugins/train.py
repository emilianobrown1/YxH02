from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from . import get_user, YxH

# Troop Training Costs and Time
TRAINING_DETAILS = {
    "shinobi": {"cost": 1000000, "time": 5},  # 5 minutes
    "wizard": {"cost": 2000000, "time": 10},  # 10 minutes
    "sensei": {"cost": 3000000, "time": 15}   # 15 minutes
}

# Command to start troop training
@Client.on_message(filters.command("train"))
@YxH()
async def train_troops(_, m, u):
    user_id = message.from_user.id
    user = await db.get_user(user_id)  # Get user data from the database
    
    # Check if the user has enough gold
    markup = troop_selection_markup()
    await message.reply("Select the troop type to train:", reply_markup=markup)

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
    user = await db.get_user(user_id)
    
    # Store the troop type for the next step
    user.active_troop_type = troop_type
    await db.update_user(user)
    
    await callback_query.message.edit("How many troops would you like to train? (1 to 3)")
    
@Client.on_message(filters.regex(r"^[1-3]$"))
async def confirm_training(client, message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)  # Get user data from the database
    
    # Retrieve the active troop type and training count
    troop_type = user.active_troop_type
    troop_count = int(message.text)
    
    # Check for sufficient gold
    cost_per_troop = TRAINING_DETAILS[troop_type]["cost"]
    total_cost = cost_per_troop * troop_count
    
    if user.gold < total_cost:
        await message.reply(f"Insufficient gold! You need {total_cost} gold.")
        return
    
    # Deduct gold and start training
    user.gold -= total_cost
    user.troops[troop_type] += troop_count
    await db.update_user(user)
    
    # Start the training process (asynchronously)
    await message.reply(f"Training {troop_count} {troop_type}s started!")
    
    # Time to train each troop
    training_time = TRAINING_DETAILS[troop_type]["time"] * 60  # Convert to seconds
    
    # Notify user when training is completed
    await asyncio.sleep(training_time)
    await message.reply(f"{troop_count} {troop_type}s have finished training!")
    
    # Clear active troop type after training
    user.active_troop_type = None
    await db.update_user(user)