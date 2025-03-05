import random
import asyncio
from pyrogram import Client, filters
from ..Class.user import User
from ..Database.users import get_user
from ..Class.chat import Chat
from ..Database.chats import get_chat
from ..universal_decorator import YxH

# Define available powers
POWERS = [
    "Darkness Shadow", "Frost Snow", "Thunder Storm",
    "Nature Ground", "Flame Heat Inferno", "Aqua Jet",
    "Strength", "Speed"
]

# Dictionary to track message counts per user
message_tracker = {}
message_lock = asyncio.Lock()  # Lock for thread-safe updates

@Client.on_message(filters.command("startpower"))
@YxH()
async def start_tracking(_, m, user):
    if user.barracks_count == 0:
        await m.reply_text("❌ You need to build a barrack first using /barracks before tracking power.")
        return
    
    async with message_lock:
        message_tracker[user.user.id] = 0
    await m.reply_text("✅ Power tracking started! Send 100 messages to unlock a new power.")

@Client.on_message(filters.text & filters.group & filters.command)  # Fixed filter
@YxH()
async def count_messages(_, m, user):
    if user.user.id not in message_tracker:
        return  # User hasn't started tracking

    async with message_lock:
        message_tracker[user.user.id] += 1
        if message_tracker[user.user.id] >= 100:  # Use >= to handle potential overshooting
            await m.reply_text("🎉 You've sent 100 messages! Use /getpower to claim your power.")
            del message_tracker[user.user.id]  # Prevent further counting after reaching 100
    
@Client.on_message(filters.command("getpower"))
@YxH()
async def claim_power(_, m, user):
    if user.user.id not in message_tracker or message_tracker[user.user.id] < 100:
        await m.reply_text("❌ You haven't reached 100 messages yet. Keep sending messages!")
        return
    
    if user.gems < 35000:
        await m.reply_text("❌ You need 35,000 gems to claim a power.")
        return

    # Get user's current power count
    total_power = sum(user.power.values())
    if total_power >= user.barracks_count * 3:
        await m.reply_text("❌ Your barracks have reached the maximum power limit.")
        return

    # Select a random power
    new_power = random.choice(POWERS)
    user.power[new_power] += 1
    user.gems -= 35000  # Deduct gems

    try:
        await user.update()  # Update user in the database
    except Exception as e:
        await m.reply_text("❌ An error occurred while updating your data. Please try again.")
        return

    # Reset message count for this user
    async with message_lock:
        del message_tracker[user.user.id]

    await m.reply_text(f"🔥 You have received **{new_power}**! It has been added to your barracks.")

@Client.on_message(filters.command("status"))
@YxH()
async def user_status(_, m, user):
    messages_sent = message_tracker.get(user.user.id, 0)
    total_power = sum(user.power.values())
    power_limit = user.barracks_count * 3

    status_message = (
        f"📊 **Status**\n"
        f"Messages Sent: {messages_sent}/100\n"
        f"Gems: {user.gems}\n"
        f"Powers: {total_power}/{power_limit}\n"
    )
    await m.reply_text(status_message)