from . import db
import pickle

tictactoe_db = db.tictactoe

async def add_tictactoe_game(user_id, result):
    """Stores the Tic-Tac-Toe game result in the database."""
    game_data = {"user_id": user_id, "result": result}
    await tictactoe_db.insert_one(game_data)

async def get_tictactoe_wins(user_id):
    """Fetches the number of Tic-Tac-Toe wins for a user."""
    count = await tictactoe_db.count_documents({"user_id": user_id, "result": "win"})
    return count
