from .Database.users import get_user
from .Class.user import User

attr = []

def init_attr_list():
  global attr
  if not attr:
    d = dir(User)
    for x in d:
      if not callable(x):
        attr.append(x)

async def load_attr(user_id: int):
  ex_user = User()
  user = await get_user(user_id)
  user_attr = 
