from ..Database.wordle import db
from .user import User
import time
import pickle

class wordle:
    def __init__(self, user: User):
        self.user = user
        self.wordle_daily_limit = 20

    async def update_user_crystals(self, crystals: int):
        self.user.crystals += crystals
        await self.user.update()


async def get_user(user_id):
    data = await db.users.find_one({'user_id': user_id})
    if data and 'info' in data:
        user_info = pickle.loads(data['info'])
        user = User(user_info.user)
        user.__dict__.update(user_info.__dict__)
        return user
    return None

