from YxH.Database import db
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
    self.wbonus = {} # {week: [False: Crystal, False: Gems, False: Gold]}
    self.dbonus = {} # {date: False}
    self.blocked = False
    self.treasure_state = False # Locked
    self.treasure = [] # [coins, gems, crystals]
    self.store = {} # {date: [id1, id2, id3]}
    self.store_purchases = {} # {date: [False, False, False]}
    self.gender = 0 # {0: None, 1: Male, -1: Female}
    self.init_time = time.time() # now
    self.words = {} # {chat_id: words}
    self.rented_items = {} # {item: time}
    self.spins = {} # {date-hour: 0}
    self.clan_id = None
    self.deals = {}
    self.mine = {} # {date-hour: 0}
    self.shield = [] # [shield_time, time.time() object]
    self.latest_defend = None # time.time() object
    self.favourite_character = None # char_id
    self.gifts = 0 # no.of gifts can be gifted
    self.convertx = {} # {date: "converted"}
    self.current_scramble = None
    self.current_scramble_answer = None
    self.scramble_completion = {} # {date: False}
    self.scramble_progress = {'incorrect_attempts': 0, 'stops': 0, 'skips': 0, 'count': 0, 'completed': False, 'blocked_until': None}
    # Dev Requirements.
    self.gl = ["Other", "Haru🧍‍♂", "Yoon🧍‍♀"]
    self.max_gems = 5_000_000
    self.max_gold = 1_000_000_000_0

  async def update(self):
    self.gems == self.max_gems if self.gems > self.max_gems else self.gems
    self.gold == self.max_gold if self.gold > self.max_gold else self.gold
    await db.users.update_one(
      {'user_id': self.user.id},
      {'$set': {'info': pickle.dumps(self)}},
      upsert=True
    )

  def get_old(self) -> int:
    return int((time.time() - self.init_time) / 86400)

def skip(self):  
        self.scramble_progress['skips'] += 1  
        self.daily_skips += 1  
        self.scramble_progress['count'] = 0  
        self.scramble_completion.pop(datetime.date.today(), None)  
  
   