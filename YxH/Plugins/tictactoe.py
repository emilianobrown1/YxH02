from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from ..Class.user import User
from ..Database.users import get_user
from ..Database.tictactoe import add_tictactoe_game
from ..universal_decorator import YxH

class TicTacToeGame:
    def __init__(self):
        self.games = {}

    def create(self, chat_id, p1, p2):
        self.games[chat_id] = {
            "p1": p1.id, "p1_name": p1.first_name,
            "p2": p2.id, "p2_name": p2.first_name,
            "board": [["⬜"]*3 for _ in range(3)],
            "turn": p1.id
        }
    
    def get(self, chat_id):
        return self.games.get(chat_id)
    
    def delete(self, chat_id):
        if chat_id in self.games:
            del self.games[chat_id]

game_manager = TicTacToeGame()

def create_board(board, chat_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(board[i][j], callback_data=f"ttt_{chat_id}_{i}_{j}") 
         for j in range(3)]
        for i in range(3)
    ])

def check_winner(board):
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "⬜":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "⬜":
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "⬜":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "⬜":
        return board[0][2]
    # Check draw
    if all(cell != "⬜" for row in board for cell in row):
        return "draw"
    return None

@Client.on_message(filters.command(["ttt", "tictactoe"]))
@YxH(group=True, private=False)
async def start_game(client, message: Message, user: User):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply("🔁 Reply to a user to start a game!")
    
    p1 = message.from_user
    p2 = message.reply_to_message.from_user
    
    if p1.id == p2.id:
        return await message.reply("🔄 You can't play against yourself!")
    if p2.is_bot:
        return await message.reply("🤖 Can't play against bots!")
    
    chat_id = message.chat.id
    if game_manager.get(chat_id):
        return await message.reply("🎮 Game already in progress!")
    
    game_manager.create(chat_id, p1, p2)
    game = game_manager.get(chat_id)
    
    await message.reply(
        f"❌ {p1.first_name} vs ⭕ {p2.first_name}\n"
        f"{p1.first_name}'s turn!",
        reply_markup=create_board(game['board'], chat_id)
    )

@Client.on_message(filters.command("forfeit"))
@YxH(group=True)
async def forfeit_game(client, message: Message, user: User):
    chat_id = message.chat.id
    game = game_manager.get(chat_id)

    if not game or message.from_user.id not in [game['p1'], game['p2']]:
        return await message.reply("🚫 No active game to forfeit!")

    # Determine winner and loser
    if message.from_user.id == game['p1']:
        winner_id, winner_name = game['p2'], game['p2_name']
        loser_id = game['p1']
    else:
        winner_id, winner_name = game['p1'], game['p1_name']
        loser_id = game['p2']

    # Get winner's User object
    winner_user = await get_user(winner_id)
    
    # Add crystal reward
    try:
        await winner_user.add_crystals(2)  # Use the new method
        await winner_user.update()  # Ensure update is called
        await add_tictactoe_game(winner_id, loser_id, "forfeit")
    except Exception as e:
        print(f"Error updating crystals: {e}")
        return await message.reply("❌ Could not process reward!")

    # Cleanup game state
    game_manager.delete(chat_id)
    
    await message.reply(
        f"🏳️ {message.from_user.first_name} forfeited!\n"
        f"🎉 {winner_name} wins and receives 2 crystals! 💎"
    )