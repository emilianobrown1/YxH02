from ..Database.wordle import db
from .user import User
import time
import pickle

class wordle:
    def __init__(self, user: User):
        self.user = user
        self.wordle_daily_limit = 20

        async def update(self):
        await self.user.update()

    async def update_user_crystals(self, crystals: int):
        self.user.crystals += crystals
        await self.user.update()

