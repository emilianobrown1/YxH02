from pyrogram import Client, filters
import asyncio
import time
from ..Class.user import User
from ..Class.barracks import BarracksManager  # If direct access needed
from .. import YxH  # Assuming YxH is in parent __init__.py

async def start_training(m, troop_type):
    user = await get_user(m.from_user.id)
    bm = user.barracks

    # Process completed trainings first
    completed = bm.process_completed_trainings()
    if sum(completed.values()) > 0:
        await user.update()

    # Calculate possible training
    try:
        gold_cost, duration = bm.start_training(
            troop_type=troop_type,
            quantity=5 * len(user.barracks.barracks),  # Max 5 per barrack
            user_gold=user.gold
        )
    except ValueError:
        return await m.reply("❌ Invalid troop type!")

    if gold_cost == 0:
        return await m.reply("❌ Not enough gold or barracks capacity!")

    # Deduct gold and update
    user.gold -= gold_cost
    await user.update()

    # Format response
    minutes = int(duration // 60)
    await m.reply(
        f"⚡ Training started!\n"
        f"🔢 Troops: {gold_cost // TRAINING_DETAILS[troop_type]['cost']}\n"
        f"⏳ Duration: {minutes} minutes\n"
        f"💸 Cost: {gold_cost:,} 🪙"
    )
