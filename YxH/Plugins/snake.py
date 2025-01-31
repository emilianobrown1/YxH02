from pyrogram import Client, filters
from ..Class.user import User
from ..Utils.snake import 


@Client.on_message(filters.command(["snake", "snakebattle"]))
@YxH(group=True)
async def start_snake(client, message: Message, user: User):
    chat_id = message.chat.id
    if snake_manager.get_game(chat_id):
        return await message.reply("🐍 Game already running!")
        
    game = snake_manager.new_game(chat_id)
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("Join Battle 🐍", callback_data=f"snake_join_{chat_id}")]])
    
    await message.reply(
        "🐍 **Snake Battle Arena**\n"
        "Players: 0/4\n"
        "Use arrows to move!\n"
        "Last surviving snake wins 15 crystals! 💎",
        reply_markup=markup
    )