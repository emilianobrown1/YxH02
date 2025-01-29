from datetime import datetime
from . import db

tictactoe_db = db.tictactoe

async def add_tictactoe_game(winner_id, loser_id, result):
    """Record Tic-Tac-Toe game result"""
    await tictactoe_db.insert_one({
        "winner": winner_id,
        "loser": loser_id,
        "result": result,
        "timestamp": datetime.now()
    })

async def get_tictactoe_stats(user_id):
    """Get player statistics"""
    return {
        "wins": await tictactoe_db.count_documents({"winner": user_id}),
        "losses": await tictactoe_db.count_documents({"loser": user_id}),
        "draws": await tictactoe_db.count_documents({
            "$or": [{"winner": user_id}, {"loser": user_id}],
            "result": "draw"
        })
    }