from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from asyncio import sleep
from typing import Dict, Any
from dataclasses import dataclass
from ..Database.users import get_user
import time

@dataclass
class TroopConfig:
    cost: int
    training_time: int  # in minutes
    emoji: str
    power: int
    description: str

# Configuration for troops, powers, and beasts
TROOP_CONFIGS = {
    "shinobi": TroopConfig(1000000, 5, "🥷", 100, "Stealthy warrior with high speed"),
    "wizard": TroopConfig(2000000, 10, "🧙", 150, "Powerful magic user"),
    "sensei": TroopConfig(3000000, 15, "🧝", 200, "Master of martial arts"),
}

POWER_CONFIGS = {
    "hammer": TroopConfig(500000, 3, "🔨", 50, "Crushes enemies with sheer force"),
    "ice": TroopConfig(800000, 4, "❄️", 80, "Freezes opponents to immobilize them"),
    "lightning": TroopConfig(1200000, 6, "⚡", 120, "Strikes with a powerful bolt"),
}

BEAST_CONFIGS = {
    "dragon": TroopConfig(5000000, 20, "🐉", 500, "A fierce and powerful fire-breathing dragon"),
    "phoenix": TroopConfig(3000000, 15, "🦅", 300, "A mystical bird that rises from ashes"),
    "tiger": TroopConfig(2000000, 10, "🐅", 200, "A fast and agile beast with sharp claws"),
}

class TrainingManager:
    def __init__(self, max_concurrent_trainings: int = 3):
        self.max_trainings = max_concurrent_trainings

    def can_start_training(self, user: Any) -> bool:
        return len(user.barracks) < self.max_trainings

    async def start_training(self, user: Any, category: str, item_type: str) -> bool:
        config = self.get_config(category, item_type)
        if not self.can_start_training(user) or not config or user.gold < config.cost:
            return False

        training_entry = {
            "type": item_type,
            "category": category,
            "start_time": time.time(),
            "end_time": time.time() + (config.training_time * 60),
        }
        user.barracks.append(training_entry)
        user.gold -= config.cost
        await user.update()
        return True

    async def complete_training(self, user: Any, training_index: int) -> None:
        if 0 <= training_index < len(user.barracks):
            training = user.barracks[training_index]
            item_type = training["type"]
            category = training["category"]
            target_dict = getattr(user, category)  # e.g., user.troops, user.powers, or user.beasts
            target_dict[item_type] = target_dict.get(item_type, 0) + 1
            user.barracks.pop(training_index)
            await user.update()

    @staticmethod
    def get_config(category: str, item_type: str) -> TroopConfig:
        return {
            "troops": TROOP_CONFIGS,
            "powers": POWER_CONFIGS,
            "beasts": BEAST_CONFIGS,
        }.get(category, {}).get(item_type)

    @staticmethod
    def create_training_keyboard(category: str) -> InlineKeyboardMarkup:
        configs = {
            "troops": TROOP_CONFIGS,
            "powers": POWER_CONFIGS,
            "beasts": BEAST_CONFIGS,
        }.get(category, {})
        buttons = []
        row = []
        for item_type, config in configs.items():
            button = InlineKeyboardButton(
                f"{config.emoji} {item_type.capitalize()} ({config.cost:,} gold)",
                callback_data=f"train_{category}_{item_type}",
            )
            row.append(button)
            if len(row) == 2:
                buttons.append(row)
                row = []

        if row:
            buttons.append(row)
        buttons.append([InlineKeyboardButton("ℹ️ Info", callback_data=f"{category}_info")])
        return InlineKeyboardMarkup(buttons)

    def get_training_status(self, user: Any) -> str:
        if not user.barracks:
            return "No items currently training!"

        current_time = time.time()
        status = "🏰 Current Training Status:\n\n"
        for i, training in enumerate(user.barracks):
            config = self.get_config(training["category"], training["type"])
            remaining_time = max(0, training["end_time"] - current_time)
            remaining_minutes = int(remaining_time / 60)
            status += (
                f"{i+1}. {config.emoji} {training['type'].capitalize()} ({training['category'].capitalize()})\n"
                f"   ⏳ {remaining_minutes} minutes remaining\n"
            )
        return status

@Client.on_message(filters.command("train"))
async def train_items(client: Client, message: Message, user: Any) -> None:
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⚔️ Troops", callback_data="train_category_troops")],
            [InlineKeyboardButton("🪄 Powers", callback_data="train_category_powers")],
            [InlineKeyboardButton("🐾 Beasts", callback_data="train_category_beasts")],
        ]
    )
    await message.reply("Select a category to train:", reply_markup=keyboard)

@Client.on_callback_query(filters.regex(r"^train_category_"))
async def select_training_category(client: Client, callback_query: CallbackQuery) -> None:
    category = callback_query.data.split("_")[2]
    training_manager = TrainingManager()
    keyboard = training_manager.create_training_keyboard(category)
    await callback_query.message.edit_text(f"Select an item to train in {category.capitalize()}:", reply_markup=keyboard)

@Client.on_callback_query(filters.regex(r"^train_"))
async def process_training(client: Client, callback_query: CallbackQuery, user: Any) -> None:
    _, category, item_type = callback_query.data.split("_")
    training_manager = TrainingManager()
    config = training_manager.get_config(category, item_type)

    if not config:
        await callback_query.answer("Invalid item type!", show_alert=True)
        return

    if not training_manager.can_start_training(user):
        await callback_query.answer("Barracks are full! Complete current training to free up space.", show_alert=True)
        return

    if user.gold < config.cost:
        await callback_query.answer(f"Not enough gold! You need {config.cost:,} gold.", show_alert=True)
        return

    if await training_manager.start_training(user, category, item_type):
        progress_message = await callback_query.message.reply(
            f"⏳ Training {config.emoji} {item_type.capitalize()}...\nTime remaining: {config.training_time} minutes"
        )

        training_index = len(user.barracks) - 1
        await sleep(config.training_time * 60)
        await training_manager.complete_training(user, training_index)

        await progress_message.edit_text(
            f"✅ Training completed!\nAdded 1 {config.emoji} {item_type.capitalize()} to your {category.capitalize()}."
        )
    else:
        await callback_query.answer("Failed to start training!", show_alert=True)

@Client.on_message(filters.command("my_barracks"))
async def show_barracks(client: Client, message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)

    if not user:
        await message.reply("You need to start the bot first.")
        return

    training_manager = TrainingManager()
    current_trainings = training_manager.get_training_status(user)

    barracks_text = (
        f"🏰 Your Barracks\n\n"
        f"Current Trainings:\n{current_trainings}\n\n"
        f"Troops:\n"
    )

    for troop_type, config in TROOP_CONFIGS.items():
        barracks_text += f"{config.emoji} {troop_type.capitalize()}: {user.troops.get(troop_type, 0)}\n"

    barracks_text += "\nPowers:\n"
    for power_type, config in POWER_CONFIGS.items():
        barracks_text += f"{config.emoji} {power_type.capitalize()}: {user.powers.get(power_type, 0)}\n"

    barracks_text += "\nBeasts:\n"
    for beast_type, config in BEAST_CONFIGS.items():
        barracks_text += f"{config.emoji} {beast_type.capitalize()}: {user.beasts.get(beast_type, 0)}\n"

    try:
        await message.reply_photo("Images/barrack.jpg", caption=barracks_text)
    except Exception:
        await message.reply(barracks_text)