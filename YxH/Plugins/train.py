from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncio import sleep
from ..Database.users import get_user
from ...universal_decorator import YxH


@Client.on_message(filters.command("train"))
@YxH(private=True)
async def train_troops(_, message, user):
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
@YxH(private=True)
async def process_training(_, callback_query, user):
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
    user.update()

    await callback_query.answer(f"Training 1 {troop_type.capitalize()} started!")
    await callback_query.message.reply(f"Training started! It will take {training_time} minutes.")

    # Wait for training to complete
    await sleep(training_time * 60)
    user.barracks[troop_type] -= 1
    user.troops[troop_type] += 1
    user.update()

    await callback_query.message.reply(f"Training of 1 {troop_type.capitalize()} completed!")


@Client.on_message(filters.command("my_barracks"))
@YxH(private=True)
async def show_barracks(_, message, user):
    barracks_text = (
        f"🏰 Your Armoury\n\n"
        f"Troops:\n"
        f"Shinobi 🥷: {user.troops['shinobi']}\n"
        f"Wizard 🧙: {user.troops['wizard']}\n"
        f"Sensei 🧝: {user.troops['sensei']}\n\n"
        f"Powers:\n"
        f"Hammer 🔨: {user.powers['Hammer']}\n"
        f"Ice ❄️: {user.powers['ice']}\n"
        f"Lightning ⚡: {user.powers['lightning']}\n\n"
        f"Beasts:\n"
        f"Dragon 🐉: {user.beasts['dragon']}\n"
        f"Phoenix 🦅: {user.beasts['phoenix']}\n"
        f"Tiger 🐅: {user.beasts['tiger']}\n"
    )
    await message.reply_photo(
        "Images/barrack.jpg",
        caption=barracks_text
    )