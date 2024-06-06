from .Database.users import get_user
from .Database.chats import get_chat
from .Database.clan import get_clan
from .Class import User, Chat, Clan

ex_user = User('YxH')
ex_chat = Chat('YxH')
ex_clan = Clan(-69, "YxH", 0)

attr = [x for x in dir(ex_user) if not callable(x)]
chat_attr = [x for x in dir(ex_chat) if not callable(x)]
clan_attr = [x for x in dir(ex_clan) if not callable(x)]

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
  
async def load_clan_attr(clan_id: int) -> Clan:
  clan = await get_clan(clan_id)
  for x in clan_attr:
    if hasattr(clan, x):
      continue
    setattr(clan, x, getattr(ex_clan, x))
  await clan.update()
  return clan