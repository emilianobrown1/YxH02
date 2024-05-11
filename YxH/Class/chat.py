from ..Database import db
import pickle

class Chat:
    def __init__(self, chat):
        self.chat = chat
        self.fw_cooldown = 25
        self.fw_status: str = ''
        self.words = {} # {user_id: words}

    async def update(self):
        await db.chats.update_one({'chat_id': self.chat.id}, {'$set': {'info': pickle.dumps(self)}}, upsert=True)
        return self