from pyrogram.types import InlineKeyboardButton
import random

class SnakeGameManager:
    def __init__(self):
        self.games = {}
        
    def new_game(self, chat_id):
        self.games[chat_id] = {
            'grid_size': 10,
            'walls': [(i,j) for i in [0,9] for j in range(10)] + [(i,0) for i in range(1,9)] + [(i,9) for i in range(1,9)],
            'food': None,
            'free_spaces': [(i,j) for i in range(1,9) for j in range(1,9)],
            'players': {},
            'start_time': time.time()
        }
        self.games[chat_id]['food'] = random.choice(self.games[chat_id]['free_spaces'])
        return self.games[chat_id]
        
    def get_game(self, chat_id):
        return self.games.get(chat_id)
        
    def end_game(self, chat_id):
        if chat_id in self.games:
            del self.games[chat_id]

def create_snake_board(game):
    board = []
    for i in range(10):
        row = []
        for j in range(10):
            pos = (i,j)
            if pos in game['walls']:
                row.append(InlineKeyboardButton("🧱", callback_data="snake_wall"))
            elif pos == game['food']:
                row.append(InlineKeyboardButton("🍎", callback_data="snake_food"))
            else:
                for pid, p in game['players'].items():
                    if pos == p['body'][0]:
                        row.append(InlineKeyboardButton("🐍", callback_data=f"snake_dir_{game['chat_id']}_head"))
                    elif pos in p['body']:
                        row.append(InlineKeyboardButton("🟢", callback_data=f"snake_dir_{game['chat_id']}_body"))
                if not row or row[-1].text == "⬛":
                    row.append(InlineKeyboardButton("⬛", callback_data="snake_move"))
        board.append(row)
        
    # Add control buttons
    board.append([
        InlineKeyboardButton("⬆️", callback_data=f"snake_dir_{game['chat_id']}_up"),
        InlineKeyboardButton("⬇️", callback_data=f"snake_dir_{game['chat_id']}_down")
    ])
    board.append([
        InlineKeyboardButton("⬅️", callback_data=f"snake_dir_{game['chat_id']}_left"),
        InlineKeyboardButton("➡️", callback_data=f"snake_dir_{game['chat_id']}_right")
    ])
    board.append([InlineKeyboardButton("Quit ❌", callback_data=f"snake_quit_{game['chat_id']}")])
    
    return board