from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncio import sleep
import datetime

@Client.on_message(filters.command("train"))
async def train_troops(client, message):
    user = get_user(message.from_user.id)  # Fetch user data
    if not user:
        await message.reply("User data not found. Please register first.")
        return

    # Training options
    troop_selection = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Shinobi 🥷", callback_data="train_shinobi"),
            InlineKeyboardButton("Wizard 🧙", callback_data="train_wizard"),
            InlineKeyboardButton("Sensei 🧝", callback_data="train_sensei")
        ]
    ])

    await message.reply("Select the type of troop to train:", reply_markup=troop_selection)


@Client.on_callback_query(filters.regex(r"train_(shinobi|wizard|sensei)"))
async def process_training(client, callback_query):
    user = get_user(callback_query.from_user.id)
    if not user:
        await callback_query.answer("User data not found. Please register first.", show_alert=True)
        return

    troop_type = callback_query.data.split("_")[1]
    costs = {"shinobi": 1000000, "wizard": 2000000, "sensei": 3000000}
    times = {"shinobi": 5, "wizard": 10, "sensei": 15}
    gold_needed = costs[troop_type]
    training_time = times[troop_type]

    if user.gold < gold_needed:
        await callback_query.answer(f"Not enough gold! You need {gold_needed} gold.", show_alert=True)
        return

    # Check barrack capacity
    if sum(user.barracks.values()) >= 3:
        await callback_query.answer("Barrack is full! Complete current training to free up space.", show_alert=True)
        return

    # Deduct gold and start training
    user.gold -= gold_needed
    user.barracks[troop_type] += 1
    await user.update()

    await callback_query.answer(f"Training 1 {troop_type.capitalize()} 🥷 started!")
    await callback_query.message.reply(f"Training started! It will take {training_time} minutes.")
    
    # Wait for training to complete
    await sleep(training_time * 60)
    user.barracks[troop_type] -= 1
    user.troops[troop_type] += 1
    await user.update()

    await callback_query.message.reply(f"Training of 1 {troop_type.capitalize()} 🥷 completed!")

---

#### **My Barracks Command**
```python
@Client.on_message(filters.command("my_barracks"))
async def show_barracks(client, message):
    user = get_user(message.from_user.id)
    if not user:
        await message.reply("User data not found. Please register first.")
        return

    barracks_text = (
        f"🏰 **Your Armoury**\n\n"
        f"**Troops:**\n"
        f"Shinobi 🥷: {user.troops['shinobi']}\n"
        f"Wizard 🧙: {user.troops['wizard']}\n"
        f"Sensei 🧝: {user.troops['sensei']}\n\n"
        f"**Powers:**\n"
        f"Power of Hammer : {user.powers['Power of Hammer']}\n"
        f"Ice ❄️: {user.powers['ice']}\n"
        f"Lightning ⚡: {user.powers['lightning']}\n\n"
        f"**Beasts:**\n"
        f"Dragon 🐉: {user.beasts['dragon']}\n"
        f"Phoenix 🦅: {user.beasts['phoenix']}\n"
        f"Tiger 🐅: {user.beasts['tiger']}\n"
    )

    await message.reply_photo(
        "barrack.jpg",
        caption=barracks_text
    )