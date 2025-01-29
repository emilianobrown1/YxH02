from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ..Class.user import User
from ..Database.users import get_user
from ..Database.tictactoe import add_tictactoe_game
from ..universal_decorator import YxH
import traceback

# Game state manager
class TicTacToeGame:
    def __init__(self):
        self.games = {}

    def create_game(self, chat_id, player1, player2):
        self.games[chat_id] = {
            "player1": player1.id,
            "player2": player2.id,
            "player1_name": player1.first_name,
            "player2_name": player2.first_name,
            "board": [["⬜"] * 3 for _ in range(3)],
            "turn": player1.id,
            "message_id": None
        }
    
    def get_game(self, chat_id):
        return self.games.get(chat_id)
    
    def delete_game(self, chat_id):
        if chat_id in self.games:
            del self.games[chat_id]

game_manager = TicTacToeGame()

def create_board_markup(board, chat_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(board[i][j], callback_data=f"ttt_move_{chat_id}_{i}_{j}") 
         for j in range(3)]
        for i in range(3)
    ])

def check_victory(board):
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
@YxH(private=False)
async def start_tictactoe(client, message, user):
    try:
        # Validate reply target
        if not message.reply_to_message or not message.reply_to_message.from_user:
            return await message.reply("🔁 Please reply to a user's message to start the game!")
        
        player1 = message.from_user
        player2 = message.reply_to_message.from_user

        # Prevent invalid matches
        if player2.is_bot:
            return await message.reply("🤖 You can't play against bots!")
        if player1.id == player2.id:
            return await message.reply("🔄 You can't play against yourself!")

        chat_id = message.chat.id
        
        # Check existing games
        if game_manager.get_game(chat_id):
            return await message.reply("🎮 There's already an active game in this chat!")

        # Initialize new game
        game_manager.create_game(chat_id, player1, player2)
        game = game_manager.get_game(chat_id)

        # Send initial game message
        msg = await message.reply(
            f"🎮 Tic-Tac-Toe: {player1.first_name} (❌) vs {player2.first_name} (⭕)\n"
            f"Current turn: {player1.first_name}",
            reply_markup=create_board_markup(game['board'], chat_id)
        )
        
        # Store message ID for updates
        game['message_id'] = msg.id

    except Exception as e:
        traceback.print_exc()
        await message.reply(f"❌ Error starting game: {str(e)}")

@Client.on_callback_query(filters.regex("^ttt_move_"))
async def handle_move(client, query: CallbackQuery):
    try:
        _, _, chat_id, row, col = query.data.split('_')
        chat_id = int(chat_id)
        row = int(row)
        col = int(col)

        game = game_manager.get_game(chat_id)
        if not game:
            return await query.answer("Game expired or not found!", show_alert=True)

        player_id = query.from_user.id
        valid_players = [game['player1'], game['player2']]
        
        # Validate player
        if player_id not in valid_players:
            return await query.answer("You're not in this game!", show_alert=True)
        if player_id != game['turn']:
            return await query.answer("Wait for your turn!", show_alert=True)

        # Validate move
        if game['board'][row][col] != "⬜":
            return await query.answer("Invalid move!", show_alert=True)

        # Update board
        symbol = "❌" if player_id == game['player1'] else "⭕"
        game['board'][row][col] = symbol

        # Check game status
        result = check_victory(game['board'])
        if result:
            if result == "draw":
                text = "🤝 It's a draw!"
            else:
                winner_id = game['player1'] if result == "❌" else game['player2']
                winner_name = game['player1_name'] if result == "❌" else game['player2_name']
                
                # Update database
                try:
                    winner_user = await get_user(winner_id)
                    await winner_user.add_tictactoe_win()
                    await add_tictactoe_game(winner_id, "win")
                    text = f"🎉 {winner_name} wins! +100,000 💎"
                except Exception as e:
                    traceback.print_exc()
                    text = f"🏆 {winner_name} wins! (Database update failed)"

            await query.message.edit(
                text=text,
                reply_markup=create_board_markup(game['board'], chat_id)
            )
            game_manager.delete_game(chat_id)
            return

        # Switch turns
        game['turn'] = game['player2'] if game['turn'] == game['player1'] else game['player1']
        current_player = game['player1_name'] if game['turn'] == game['player1'] else game['player2_name']

        # Update game message
        await query.message.edit(
            text=f"🎮 Tic-Tac-Toe\nCurrent turn: {current_player}",
            reply_markup=create_board_markup(game['board'], chat_id)
        )
        await query.answer()

    except Exception as e:
        traceback.print_exc()
        await query.answer("⚠️ Error processing move!", show_alert=True)

@Client.on_message(filters.command("forfeit"))
@YxH(private=False)
async def forfeit_game(client, message, user):
    try:
        chat_id = message.chat.id
        game = game_manager.get_game(chat_id)
        
        if not game:
            return await message.reply("No active game to forfeit!")
        
        if message.from_user.id not in [game['player1'], game['player2']]:
            return await message.reply("You're not in this game!")
        
        # Determine opponent
        opponent_id = game['player1'] if message.from_user.id == game['player2'] else game['player2']
        opponent_name = game['player1_name'] if opponent_id == game['player1'] else game['player2_name']

        # Update database
        try:
            winner_user = await get_user(opponent_id)
            await winner_user.add_tictactoe_win()
            await add_tictactoe_game(opponent_id, "win")
            db_text = "+100,000 💎"
        except Exception as e:
            traceback.print_exc()
            db_text = "(Database update failed)"

        # Cleanup and notify
        game_manager.delete_game(chat_id)
        await message.reply(
            f"🏳️ {message.from_user.first_name} forfeited!\n"
            f"🏆 {opponent_name} wins! {db_text}"
        )

    except Exception as e:
        traceback.print_exc()
        await message.reply("❌ Error processing forfeit!")