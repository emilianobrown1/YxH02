
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup
from ..Class.user import User
from ..Utils.snake import snake_manager
from ..Database.snake import add_snake_game
from ..universal_decorator import YxH

@Client.on_message(filters.command(["snake", "snakebattle"]))
@YxH(group=True)
async def start_snake(client: Client, message: Message, user: User):
    chat_id = message.chat.id
    if snake_manager.get_game(chat_id):
        return await message.reply("🐍 Game already running!")

    game = snake_manager.new_game(chat_id)
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("Join Battle 🐍", callback_data=f"snake_join_{chat_id}")]])

    await message.reply(
        f"🐍 **Snake Battle Arena**\n"
        f"Players: 0/4\n"
        "Use arrows to move!\n"
        "Last surviving snake wins 15 crystals! 💎",
        reply_markup=markup
    )