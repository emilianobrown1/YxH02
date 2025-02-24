from ..Database import db 
import pickle
import time

class User:
    def __init__(self, user):
        self.user = user  # Renamed from `user` to `user_id` for clarity
        self.crystals = 0
        self.gems = 0
        self.gold = 0
        self.collection = {}
        self.profile_picture = None
        self.active_bot_id = 0
        self.wbonus = {}  # {week: [False: Crystal, False: Gems, False: Gold]}
        self.dbonus = {}  # {date: False}
        self.blocked = False
        self.treasure_state = False  # Locked
        self.treasure = [0, 0, 0]  # [golds, gems, crystals]
        self.store = {}  # {date: [id1, id2, id3]}
        self.store_purchases = {}  # {date: [False, False, False]}
        self.gender = 0  # {0: None, 1: Male, -1: Female}
        self.init_time = time.time()  # now
        self.words = {}  # {chat_id: words}
        self.rented_items = {}  # {item: time}
        self.spins = {}  # {date-hour: 0}
        self.clan_id = None
        self.deals = {}
        self.mine = {}  # {date-hour: 0}
        self.shield = []  # [shield_time, time.time() object]
        self.latest_defend = None  # time.time() object
        self.favourite_character = None  # char_id
        self.gifts = 0  # no.of gifts can be gifted
        self.gifts_sent = {}  # Track daily gifts sent {date: count}
        self.invite_link = None
        self.invited_by = None
        self.partner = None 
        self.convertx = {}  # {date: "converted"}
        self.buy_crystals = {}
        self.scramble = []
        self.swap = {
            "count": 0  # Track the number of swaps
        }
        
        self.inventory = {
            "Magic Key 🗝️": 0,
            "Magic Diamond 💎": 0,
            "Magic Potion 🧪": 0,
            "Magic Stone 🪨": 0
        }
        self.magic_uses = 0  # Track magic command usage
        self.tictactoe_wins = 0  # Track Tic-Tac-Toe wins
        self.last_magic_use_time = 0
        # Dev Requirements.
        self.gl = ["Other", "Haru🧍‍♂", "Yoon🧍‍♀"]
        self.max_gems = 5_000_000
        self.max_gold = 1_000_000_000_0

    async def update_invite_link(self, link):
        self.invite_link = link
        await self.update()

    async def update(self):
        self.gems = min(self.gems, self.max_gems)
        self.gold = min(self.gold, self.max_gold)
        await db.users.update_one(
            {'user_id': self.user.id},  
            {'$set': {'info': pickle.dumps(self)}},
            upsert=True
        )

    async def add_tictactoe_win(self):
        """Increments Tic-Tac-Toe wins, gives gems, and updates the database."""
        self.tictactoe_wins += 1
        self.crystals += 2  # Reward 100,000 gems per win
        await self.update()

    async def add_crystals(self, amount: int):
        """Generic method to add crystals"""
        self.crystals += amount
        await self.update()

    def __setstate__(self, state):
        # Remove legacy attributes that no longer exist in the class
        state.pop('barracks_manager', None)  # Handle removed BarracksManager
        # Update the instance's __dict__ with the cleaned state
        self.__dict__.update(state)
        if not hasattr(self, 'new_attribute_added_after_pickling'):
            self.new_attribute_added_after_pickling = default_value  # Set default if needed
            

    def is_blocked(self):
        return self.blocked

    def block_user(self):
        self.blocked = True

    def unblock_user(self):
        self.blocked = False
        # Perform additional actions if needed
        
        # Example: Notify the user about the unblocking

    
    def get_old(self) -> int:
        return int((time.time() - self.init_time) / 86400)
