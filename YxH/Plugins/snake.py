from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ..Utils.snake import snake_manager
from ..Class.user import User
from ..universal_decorator import YxH

@Client.on_message(filters.command(["snake", "snakebattle"]))
@YxH(group=True)
async def start_snake(client: Client, message: Message, user: User):
    chat_id = message.chat.id
    if snake_manager.games.get(chat_id):
        return await message.reply("🐍 A game is already running! Use /over to end it.")
    
    game = snake_manager.new_game(chat_id, message.from_user.id)
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("🎮 Join Battle", callback_data=f"snake_join_{chat_id}")]])
    
    msg = await message.reply(
        f"🐍 **Snake Battle Arena**\n"
        f"Host: {message.from_user.first_name}\n"
        f"Players: 0/4\n"
        f"Status: Waiting for players...\n"
        f"Use /over to cancel game",
        reply_markup=markup
    )
    game['message_id'] = msg.id

@Client.on_message(filters.command("over"))
async def end_game(client: Client, message: Message):
    chat_id = message.chat.id
    game = snake_manager.games.get(chat_id)
    
    if not game:
        return await message.reply("No active game to end!")
    
    if message.from_user.id != snake_manager.creators.get(chat_id):
        return await message.reply("⚠️ Only game host can end the match!")
    
    snake_manager.end_game(chat_id)
    await message.reply("🐍 Game ended by host!")
    try:
        await client.delete_messages(chat_id, game['message_id'])
    except:
        pass