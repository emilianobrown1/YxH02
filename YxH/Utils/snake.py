import time
import random
from pyrogram.types import InlineKeyboardButton

class SnakeGameManager:
    def __init__(self):
        self.games = {}
        self.creators = {}
        self.join_timeout = 120  # 2 minutes to join

    def new_game(self, chat_id, creator_id):
        self.games[chat_id] = {
            'chat_id': chat_id,
            'creator': creator_id,
            'players': {},
            'player_order': [],
            'current_turn': 0,
            'status': 'waiting',
            'start_time': time.time(),
            'message_id': None,
            'grid_size': 10,
            'walls': self.generate_walls(),
            'food': None,
            'free_spaces': []
        }
        self.creators[chat_id] = creator_id
        self.generate_food(chat_id)
        return self.games[chat_id]

    def generate_walls(self):
        return [(i, j) for i in [0, 9] for j in range(10)] + \
               [(i, 0) for i in range(1, 9)] + \
               [(i, 9) for i in range(1, 9)]

    def update_free_spaces(self, chat_id):
        game = self.games[chat_id]
        occupied = set(game['walls'])
        for p in game['players'].values():
            occupied.update(p['body'])
        game['free_spaces'] = [(i, j) for i in range(10) for j in range(10) 
                              if (i, j) not in occupied and (i, j) != game['food']]

    def generate_food(self, chat_id):
        game = self.games[chat_id]
        game['food'] = random.choice(game['free_spaces'])
        return game['food']

    def get_current_player(self, chat_id):
        game = self.games.get(chat_id)
        if not game or game['status'] != 'playing':
            return None
        return game['player_order'][game['current_turn']]

    def next_turn(self, chat_id):
        game = self.games[chat_id]
        game['current_turn'] = (game['current_turn'] + 1) % len(game['player_order'])
        return self.get_current_player(chat_id)

    def end_game(self, chat_id):
        if chat_id in self.games:
            del self.games[chat_id]
        if chat_id in self.creators:
            del self.creators[chat_id]

    def remove_player(self, chat_id, user_id):
        game = self.games.get(chat_id)
        if game and user_id in game['players']:
            del game['players'][user_id]
            game['player_order'].remove(user_id)
            self.update_free_spaces(chat_id)

# Create a singleton instance of the game manager
snake_manager = SnakeGameManager()

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
                btn_added = False
                for pid, p in game['players'].items():
                    if pos == p['body'][0]:
                        row.append(InlineKeyboardButton("🐍", callback_data=f"snake_head_{pid}"))
                        btn_added = True
                        break
                    elif pos in p['body']:
                        row.append(InlineKeyboardButton("🟢", callback_data=f"snake_body_{pid}"))
                        btn_added = True
                        break
                if not btn_added:
                    row.append(InlineKeyboardButton("⬛", callback_data="snake_empty"))
        board.append(row)
    
    # Control buttons
    controls = [
        [
            InlineKeyboardButton("⬆️", callback_data=f"snake_dir_{game['chat_id']}_up"),
            InlineKeyboardButton("⬇️", callback_data=f"snake_dir_{game['chat_id']}_down")
        ],
        [
            InlineKeyboardButton("⬅️", callback_data=f"snake_dir_{game['chat_id']}_left"),
            InlineKeyboardButton("➡️", callback_data=f"snake_dir_{game['chat_id']}_right")
        ],
        [InlineKeyboardButton("Quit Game ❌", callback_data=f"snake_quit_{game['chat_id']}")]
    ]
    return board

# Export the manager and other necessary functions
__all__ = ['snake_manager', 'create_snake_board']