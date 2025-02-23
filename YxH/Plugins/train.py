e
from pyrogram import Client, filters
import asyncio
from ..Class.user import User
from .. import YxH

@Client.on_message(filters.command(["shinobi", "wizard", "sensei"]))
@YxH()
async def train_troops(client, m, u: User):
    try:
        troop_type = m.command[0].lower()
        bm = u.barracks_manager
        
        # Process completed trainings first
        completed = bm.process_completed_trainings()
        if sum(completed.values()) > 0:
            await u.update()

        # Calculate max possible troops
        max_troops = len(bm.barracks) * 5
        if max_troops <= 0:
            await m.reply("❌ You need at least 1 barrack!")
            return

        # Start training
        try:
            cost, duration = bm.start_training(troop_type, max_troops)
        except ValueError:
            await m.reply("❌ Invalid troop type!")
            return

        if u.gold < cost:
            await m.reply(f"💰 Insufficient gold! Need: {cost:,} 🪙")
            return

        # Deduct gold and update
        u.gold -= cost
        await u.update()

        # Send response
        minutes = int(duration // 60)
        await m.reply(
            f"⚡ Training started!\n"
            f"🔢 Quantity: {max_troops} {troop_type.capitalize()}s\n"
            f"⏳ Duration: {minutes} minutes\n"
            f"💸 Cost: {cost:,} 🪙"
        )

        # Schedule completion notification
        await asyncio.sleep(duration)
        await m.reply(f"✅ Training complete! {max_troops} {troop_type.capitalize()}s added to your barracks!")

    except Exception as e:
        await m.reply(f"❌ Error: {str(e)}")