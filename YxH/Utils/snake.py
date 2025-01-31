import time
import random
from pyrogram.types import InlineKeyboardButton

class SnakeGameManager:
    def __init__(self):
        self.games = {}

    def new_game(self, chat_id):
        self.games[chat_id] = {
            'chat_id': chat_id,
            'grid_size': 10,
            'walls': self.generate_walls(),
            'food': None,
            'players': {},
            'start_time': time.time(),
            'free_spaces': []
        }
        self.update_free_spaces(chat_id)
        self.games[chat_id]['food'] = self.generate_food(chat_id)
        return self.games[chat_id]

    def generate_walls(self):
        return [(i, j) for i in [0, 9] for j in range(10)] + \
               [(i, 0) for i in range(1, 9)] + \
               [(i, 9) for i in range(1, 9)]

    def update_free_spaces(self, chat_id):
        game = self.games[chat_id]
        occupied = set(game['walls'])
        for player in game['players'].values():
            occupied.update(player['body'])
        game['free_spaces'] = [
            (i, j) for i in range(10) for j in range(10)
            if (i, j) not in occupied and (i, j) != game['food']
        ]

    def generate_food(self, chat_id):
        return random.choice(self.games[chat_id]['free_spaces'])

    def get_game(self, chat_id):
        return self.games.get(chat_id)

    def end_game(self, chat_id):
        if chat_id in self.games:
            del self.games[chat_id]

    def remove_player(self, chat_id, user_id):
        if chat_id in self.games and user_id in self.games[chat_id]['players']:
            del self.games[chat_id]['players'][user_id]
            self.update_free_spaces(chat_id)

def create_snake_board(game):
    board = []
    for i in range(10):
        row = []
        for j in range(10):
            pos = (i, j)
            if pos in game['walls']:
                row.append(InlineKeyboardButton("🧱", callback_data="snake_wall"))
            elif pos == game['food']:
                row.append(InlineKeyboardButton("🍎", callback_data="snake_food"))
            else:
                found = False
                for pid, p in game['players'].items():
                    if pos == p['body'][0]:
                        row.append(InlineKeyboardButton("🐍", callback_data=f"snake_head_{pid}"))
                        found = True
                        break
                    elif pos in p['body']:
                        row.append(InlineKeyboardButton("🟢", callback_data=f"snake_body_{pid}"))
                        found = True
                        break
                if not found:
                    row.append(InlineKeyboardButton("⬛", callback_data="snake_empty"))
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