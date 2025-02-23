from pyrogram import Client, filters
import asyncio
import time
from . import YxH
from ..Database.users import get_user
from ..Class.user import User

TRAINING_DETAILS = {
    "shinobi": {"cost": 1000000, "time": 5},  # 5 minutes
    "wizard": {"cost": 2000000, "time": 10},  # 10 minutes
    "sensei": {"cost": 3000000, "time": 15}   # 15 minutes
}

BARRACKS_CAPACITY = 5  # Troops per barracks

# Ensure barracks storage structure is correct
def initialize_barracks(user):
    if not isinstance(user.barracks, list):
        user.barracks = []
    for i in range(len(user.barracks)):
        if not isinstance(user.barracks[i], dict):
            user.barracks[i] = {"timestamp": time.time(), "troops": {"shinobi": 0, "wizard": 0, "sensei": 0}}

# Generalized training command
async def start_training(m, troop_type):
    user_id = m.from_user.id
    user = await get_user(user_id)  # Get user data from the database
    initialize_barracks(user)

    # Check if the user has barracks
    if len(user.barracks) < 1:
        await m.reply("You don't have a barracks. Buy one to train troops.")
        return

    # Calculate max troops user can train
    max_troops = len(user.barracks) * BARRACKS_CAPACITY
    
    # Deduct gold and start training
    cost_per_troop = TRAINING_DETAILS[troop_type]["cost"]
    total_cost = cost_per_troop * max_troops
    
    if user.gold < total_cost:
        await m.reply(f"Insufficient gold! You need {total_cost} 🪙 to train {max_troops} {troop_type}s.")
        return
    
    user.gold -= total_cost
    
    # Distribute troops across barracks
    for barrack in user.barracks:
        barrack["troops"][troop_type] += BARRACKS_CAPACITY
    
    await user.update()  # Update the user's data in the database
    
    await m.reply(f"Training {max_troops} {troop_type}s started! Training time: {TRAINING_DETAILS[troop_type]['time']} minutes.")
    
    # Notify user when training is completed
    training_time = TRAINING_DETAILS[troop_type]["time"] * 60  # Convert to seconds
    await asyncio.sleep(training_time)
    await m.reply(f"{max_troops} {troop_type}s have finished training and are stored in your barracks!")

# Commands to train troops
@Client.on_message(filters.command("Shinobi"))
@YxH()
async def train_shinobi(_, m, u):
    await start_training(m, "shinobi")

@Client.on_message(filters.command("wizard"))
@YxH()
async def train_wizard(_, m, u):
    await start_training(m, "wizard")

@Client.on_message(filters.command("sensei"))
@YxH()
async def train_sensei(_, m, u):
    await start_training(m, "sensei")