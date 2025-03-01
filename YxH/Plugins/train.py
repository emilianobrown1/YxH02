from pyrogram import Client, filters
from . import get_user, YxH
import asyncio
import time

@Client.on_message(filters.command("train"))
@YxH()
async def train_troops(client, m, user):
    # Check if user has barracks
    if user.barracks_count == 0:
        await m.reply(
            "❌ You need to build barracks first with /barracks!"
        )
        return

    try:
        # Parse command
        parts = m.command
        if len(parts) < 2:
            raise ValueError
        
        troop = parts[1].capitalize()
        if troop not in ["Shinobi", "Wizard", "Sensei"]:
            raise ValueError
            
        amount = int(parts[2]) if len(parts) > 2 else 1
        amount = max(1, min(amount, 5))
        
    except (ValueError, IndexError):
        await m.reply(
                "⚔️ **Invalid Command Format**\n\n"
                "Usage: `/train [Troop] [Amount]`\n"
                "Available Troops: Shinobi, Wizard, Sensei\n"
                "Max 5 troops per batch\n\n"
                "Example: `/train Shinobi 3`"
            )
        )
        return

    # Training costs and times
    training_data = {
        "Shinobi": {"cost": 1_000_000, "time": 5},
        "Wizard": {"cost": 2_000_000, "time": 10},
        "Sensei": {"cost": 3_000_000, "time": 15}
    }

    total_cost = training_data[troop]["cost"] * amount
    total_time = training_data[troop]["time"] * amount

    # Check gold balance
    if user.gold < total_cost:
        await m.reply(
                f"💰 **Insufficient Gold!**\n\n"
                f"Required: {total_cost:,} Gold\n"
                f"Your Balance: {user.gold:,}\n\n"
                f"Train fewer troops or earn more gold!"
            )
        )
        return

    # Deduct gold and start training
    user.gold -= total_cost
    completion_time = time.time() + (total_time * 60)
    
    # Add to trainings
    user.trainings.append({
        "troop": troop,
        "amount": amount,
        "completion_time": completion_time,
        "chat_id": m.chat.id
    })
    await user.update()

    # Send confirmation
    await m.reply(
            "⚡ **Training Started!**\n\n"
            f"🛡️ Troop Type: {troop}\n"
            f"🔢 Quantity: {amount}\n"
            f"⏳ Duration: {total_time} minutes\n"
            f"💸 Gold Spent: {total_cost:,}\n\n"
            "You'll be notified when training completes!"
        )
    )

    # Schedule completion notification
    async def complete_training():
        await asyncio.sleep(total_time * 60)
        
        # Refresh user data
        current_user = await get_user(user.user.id)
        for training in current_user.trainings:
            if training["completion_time"] == completion_time:
                # Add troops
                current_user.troops[troop] += amount
                current_user.trainings.remove(training)
                await current_user.update()
                
                # Send completion message
                await client.send_message(
                    chat_id=m.chat.id,
                    text=(
                        f"🎉 **Training Complete!**\n\n"
                        f"🏆 {amount} {troop} added to your army!\n"
                        f"Total {troop}: {current_user.troops[troop]}\n\n"
                        "Ready for battle commander!"
                    )
                )
                break

    asyncio.create_task(complete_training())
  
