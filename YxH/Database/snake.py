# Database/snake.py
from datetime import datetime
from . import db

snake_db = db.snake_games

async def add_snake_game(winner_id, player_ids, start_time):
    await snake_db.insert_one({
        "winner": winner_id,
        "players": player_ids,
        "duration": datetime.now().timestamp() - start_time,
        "timestamp": datetime.now()
    })