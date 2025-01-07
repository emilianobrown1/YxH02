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

# Configuration for different troop types
TROOP_CONFIGS = {
    "shinobi": TroopConfig(1000000, 5, "🥷", 100, "Stealthy warrior with high speed"),
    "wizard": TroopConfig(2000000, 10, "🧙", 150, "Powerful magic user"),
    "sensei": TroopConfig(3000000, 15, "🧝", 200, "Master of martial arts"),
}

class TrainingManager:
    def __init__(self, max_concurrent_trainings: int = 3):
        self.max_trainings = max_concurrent_trainings

    def can_start_training(self, user: Any) -> bool:
        return len(user.barracks) < self.max_trainings

    async def start_training(self, user: Any, troop_type: str) -> bool:
        if not self.can_start_training(user):
            return False

        config = TROOP_CONFIGS.get(troop_type)
        if not config or user.gold < config.cost:
            return False

        training_entry = {
            "type": troop_type,
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
            troop_type = training["type"]
            user.troops[troop_type] = user.troops.get(troop_type, 0) + 1
            user.barracks.pop(training_index)
            await user.update()

    @staticmethod
    def create_training_keyboard() -> InlineKeyboardMarkup:
        buttons = []
        row = []
        for troop_type, config in TROOP_CONFIGS.items():
            button = InlineKeyboardButton(
                f"{config.emoji} {troop_type.capitalize()} ({config.cost:,} gold)",
                callback_data=f"train_{troop_type}",
            )
            row.append(button)
            if len(row) == 2:
                buttons.append(row)
                row = []

        if row:
            buttons.append(row)

        buttons.append([InlineKeyboardButton("ℹ️ Troop Info", callback_data="troop_info")])
        return InlineKeyboardMarkup(buttons)

    def get_training_status(self, user: Any) -> str:
        if not user.barracks:
            return "No troops currently training!"

        current_time = time.time()
        status = "🏰 Current Training Status:\n\n"
        for i, training in enumerate(user.barracks):
            config = TROOP_CONFIGS[training["type"]]
            remaining_time = max(0, training["end_time"] - current_time)
            remaining_minutes = int(remaining_time / 60)
            status += (
                f"{i+1}. {config.emoji} {training['type'].capitalize()}\n"
                f"   ⏳ {remaining_minutes} minutes remaining\n"
            )
        return status

@Client.on_message(filters.command("train"))
async def train_troops(client: Client, message: Message, user: Any) -> None:
    training_manager = TrainingManager()
    keyboard = training_manager.create_training_keyboard()
    status = training_manager.get_training_status(user)
    await message.reply(
        f"Select the type of troop to train:\n\n{status}",
        reply_markup=keyboard,
    )

@Client.on_callback_query(filters.regex(r"^train_"))
async def process_training(client: Client, callback_query: CallbackQuery, user: Any) -> None:
    training_manager = TrainingManager()
    troop_type = callback_query.data.split("_")[1]
    config = TROOP_CONFIGS.get(troop_type)

    if not config:
        await callback_query.answer("Invalid troop type!", show_alert=True)
        return

    if not training_manager.can_start_training(user):
        await callback_query.answer(
            "Barracks are full! Complete current training to free up space.",
            show_alert=True,
        )
        return

    if user.gold < config.cost:
        await callback_query.answer(
            f"Not enough gold! You need {config.cost:,} gold.",
            show_alert=True,
        )
        return

    if await training_manager.start_training(user, troop_type):
        progress_message = await callback_query.message.reply(
            f"⏳ Training {config.emoji} {troop_type.capitalize()}...\n"
            f"Time remaining: {config.training_time} minutes"
        )

        training_index = len(user.barracks) - 1
        await sleep(config.training_time * 60)
        await training_manager.complete_training(user, training_index)

        await progress_message.edit_text(
            f"✅ Training completed!\n"
            f"Added 1 {config.emoji} {troop_type.capitalize()} to your army."
        )
    else:
        await callback_query.answer("Failed to start training!", show_alert=True)

@Client.on_callback_query(filters.regex("troop_info"))
async def show_troop_info(client: Client, callback_query: CallbackQuery, user: Any) -> None:
    info_text = "📖 Troop Information:\n\n"
    for troop_type, config in TROOP_CONFIGS.items():
        info_text += (
            f"{config.emoji} {troop_type.capitalize()}\n"
            f"├ Cost: {config.cost:,} gold\n"
            f"├ Training: {config.training_time} minutes\n"
            f"├ Power: {config.power}\n"
            f"└ {config.description}\n\n"
        )

    await callback_query.answer()
    await callback_query.message.edit_text(
        info_text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back to Training", callback_data="back_to_training")]]
        ),
    )

@Client.on_callback_query(filters.regex("back_to_training"))
async def back_to_training(client: Client, callback_query: CallbackQuery, user: Any) -> None:
    training_manager = TrainingManager()
    keyboard = training_manager.create_training_keyboard()
    status = training_manager.get_training_status(user)

    await callback_query.answer()
    await callback_query.message.edit_text(
        f"Select the type of troop to train:\n\n{status}",
        reply_markup=keyboard,
    )

@Client.on_message(filters.command("my_barracks"))
async def show_barracks(client: Client, message: Message, user: Any) -> None:
    training_manager = TrainingManager()
    current_trainings = training_manager.get_training_status(user)
    barracks_text = (
        f"🏰 Your Barracks\n\n"
        f"Current Trainings:\n{current_trainings}\n\n"
        f"Troops:\n"
    )

    for troop_type, config in TROOP_CONFIGS.items():
        barracks_text += f"{config.emoji} {troop_type.capitalize()}: {user.troops.get(troop_type, 0)}\n"

    try:
        await message.reply_photo(
            "Images/barrack.jpg",
            caption=barracks_text,
        )
    except Exception:
        await message.reply(barracks_text)