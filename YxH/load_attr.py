from .Database.users import get_user
from .Database.chats import get_chat
from .Class import User, Chat

ex_user = User('YxH')
ex_chat = Chat('YxH')

attr = [x for x in dir(ex_user) if not callable(x)]
chat_attr = [x for x in dir(ex_chat) if not callable(x)]

async def load_attr(user_id: int) -> User:
  user = await get_user(user_id)
  for x in attr:
    if hasattr(user, x):
      continue
    setattr(user, x, getattr(ex_user, x))
  await user.update()
  return user

async def load_chat_attr(chat_id: int) -> Chat:
  chat = await get_chat(chat_id)
  for x in chat_attr:
    if hasattr(chat, x):
      continue
    setattr(chat, x, getattr(ex_chat, x))
  await chat.update()
  return chat