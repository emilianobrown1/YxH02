from pyrogram import Client, filters
from asyncio import sleep
from datetime import datetime
from ..Database.users import get_user
from ..Class.user import User  # Import your User class

@Client.on_message(filters.command("train"))
async def train_troops(client, message):
    user_id = message.from_user.id
    user = await get_user_data(user_id)

    # Check if user has barracks
    if not hasattr(user, "barracks") or user.barracks <= 0:
        return await message.reply_text("You don't have any barracks! Build one to train troops using /barracks.")

    # Calculate training capacity
    current_training = user.training.get("Shinobi", 0)
    max_training = user.barracks * 3  # Each barrack can train 3 shinobi
    if current_training >= max_training:
        return await message.reply_text("Your barracks are fully occupied! Wait until training is complete.")

    # Determine the number of shinobi to train
    available_slots = max_training - current_training
    shinobi_to_train = min(available_slots, 3)  # Limit training batch to 3
    user.training["Shinobi"] += shinobi_to_train
    await user.update()

    # Notify the user
    await message.reply_text(
        f"Training {shinobi_to_train} Shinobi. They will be ready in 5 minutes each."
    )

    # Simulate training time
    for _ in range(shinobi_to_train):
        await sleep(300)  # 5 minutes per shinobi
        user.training["Shinobi"] -= 1
        user.armoury["Trops"]["Shinobi"] = user.armoury["Trops"].get("Shinobi", 0) + 1
        await user.update()

    # Notify training completion
    await message.reply_text(
        f"{shinobi_to_train} Shinobi have completed training and are added to your Armoury!"
    )

async def get_user_data(user_id):
    # Fetch the user instance from the database
    user = await get_user(user_id)
    if not user:
        user = User(user_id)

    # Ensure necessary attributes exist
    if not hasattr(user, "barracks"):
        user.barracks = 0
    if "Trops" not in user.armoury:
        user.armoury["Trops"] = {}
    if not hasattr(user, "training"):
        user.training = {"Shinobi": 0}

    await user.update()
    return user
