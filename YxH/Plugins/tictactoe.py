from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ..Class.user import User
from ..Database.users import get_user
from ..Database.tictactoe import add_tictactoe_game

games = {}  # Active games {chat_id: {player1_id, player2_id, board, turn}}

# Tic-Tac-Toe Board
def create_board():
    return [["⬜"] * 3 for _ in range(3)]

def get_board_markup(board, chat_id):
    """Creates an inline keyboard for the current board state."""
    buttons = [
        [InlineKeyboardButton(board[i][j], callback_data=f"move_{chat_id}_{i}_{j}") for j in range(3)]
        for i in range(3)
    ]
    return InlineKeyboardMarkup(buttons)

def check_winner(board):
    """Checks if there's a winner."""
    for row in board:
        if row[0] == row[1] == row[2] != "⬜":
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "⬜":
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != "⬜" or board[0][2] == board[1][1] == board[2][0] != "⬜":
        return board[1][1]

    if all(cell != "⬜" for row in board for cell in row):
        return "draw"

    return None

@Client.on_message(filters.command("ttt") & filters.reply)
async def start_tictactoe(client, message):
    """Starts a Tic-Tac-Toe game with the replied user."""
    chat_id = message.chat.id
    player1_id = message.from_user.id
    player2_id = message.reply_to_message.from_user.id

    if chat_id in games:
        return await message.reply("A game is already in progress!")

    games[chat_id] = {
        "player1": player1_id,
        "player2": player2_id,
        "board": create_board(),
        "turn": player1_id,
    }

    await message.reply(
        f"🎮 Tic-Tac-Toe started between {message.from_user.first_name} (❌) and {message.reply_to_message.from_user.first_name} (⭕)\n\n"
        f"{message.from_user.first_name}, it's your turn!",
        reply_markup=get_board_markup(games[chat_id]["board"], chat_id)
    )

@Client.on_callback_query(filters.regex("^move_"))
async def handle_move(client, query: CallbackQuery):
    """Handles a player's move."""
    _, chat_id, row, col = query.data.split("_")
    chat_id, row, col = int(chat_id), int(row), int(col)

    if chat_id not in games:
        return await query.answer("Game not found!", show_alert=True)

    game = games[chat_id]
    player_id = query.from_user.id

    if player_id not in [game["player1"], game["player2"]]:
        return await query.answer("You're not in this game!", show_alert=True)

    if player_id != game["turn"]:
        return await query.answer("Not your turn!", show_alert=True)

    if game["board"][row][col] != "⬜":
        return await query.answer("Invalid move!", show_alert=True)

    symbol = "❌" if player_id == game["player1"] else "⭕"
    game["board"][row][col] = symbol

    winner = check_winner(game["board"])

    if winner:
        if winner == "draw":
            await query.message.edit_text("😲 It's a draw!")
        else:
            winner_id = game["player1"] if winner == "❌" else game["player2"]
            winner_user = await get_user(winner_id)
            await winner_user.add_tictactoe_win()
            await add_tictactoe_game(winner_id, "win")
            await query.message.edit_text(f"🎉 {query.from_user.first_name} won the game! +100,000 💎")
        del games[chat_id]
        return

    game["turn"] = game["player1"] if game["turn"] == game["player2"] else game["player2"]

    await query.message.edit_text(
        f"🎮 Tic-Tac-Toe Game\n\n{query.from_user.first_name}, it's your turn!",
        reply_markup=get_board_markup(game["board"], chat_id)
    )

@Client.on_message(filters.command("forfeit"))
async def forfeit_game(client, message):
    """Allows a player to forfeit the game."""
    chat_id = message.chat.id

    if chat_id not in games:
        return await message.reply("No active game in this chat!")

    game = games.pop(chat_id)
    opponent_id = game["player1"] if message.from_user.id == game["player2"] else game["player2"]
    winner_user = await get_user(opponent_id)
    await winner_user.add_tictactoe_win()
    await add_tictactoe_game(opponent_id, "win")

    await message.reply(f"😢 {message.from_user.first_name} forfeited! {winner_user.user.first_name} wins! 🎉")
