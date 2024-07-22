from YxH.Database import db
from YxH.Class.wordle import Wordle
import pickle
import time

class User:
    def __init__(self, user):
        self.user = user
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
        self.convertx = {}  # {date: "converted"}
        self.buy_crystals = {}
        self.scramble = []
        self.wordle = {}
        # Dev Requirements.
        self.gl = ["Other", "Haru🧍‍♂", "Yoon🧍‍♀"]
        self.max_gems = 5_000_000
        self.max_gold = 1_000_000_000_0

    async def load_from_db(self):
        data = await db.users.find_one({'user_id': self.user.id})
        if data and 'info' in data:
            db_info = pickle.loads(data['info'])
            self.__dict__.update(db_info.__dict__)

    async def update(self):
        self.gems = min(self.gems, self.max_gems)
        self.gold = min(self.gold, self.max_gold)
        await db.users.update_one(
            {'user_id': self.user.id},
            {'$set': {'info': pickle.dumps(self)}},
            upsert=True
        )

    def is_blocked(self):
        return self.blocked

    def block_user(self):
        self.blocked = True
        # Perform additional actions if needed
        # Example: Log the blocking action
        # Example: Notify the user about the blocking

    def unblock_user(self):
        self.blocked = False
        # Perform additional actions if needed
        # Example: Log the unblocking action
        # Example: Notify the user about the unblocking

    def get_old(self) -> int:
        return int((time.time() - self.init_time) / 86400)
