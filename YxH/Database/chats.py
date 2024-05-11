from . import db
import pickle

db = db.chats

async def get_chat(chat_id):
  x = await db.find_one({'chat_id': chat_id})
  if x:
    return pickle.loads(x['info'])
  return None