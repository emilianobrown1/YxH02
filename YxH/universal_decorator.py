from .Database.users import get_user
from .Utils.force_start import force_start
from .Utils.strings import block_text, negate_private_text, negate_group_text
from config import SUDO_USERS, OWNER_ID
from .load_attr import load_attr

def YxH(
  private=True,
  group=True,
  sudo=False,
  owner=False
):
  def fun(func):
    async def wrapper(_, m, *args):
      user_id = m.from_user.id
      chat_id = m.chat.id
      user = await get_user(user_id)
      if not user:
        return await force_start(m)
      if user.blocked:
        return await m.reply(block_text)
      if not private:
        if chat_id > 0:
          return await m.reply(negate_private_text)
      if not group:
        if chat_id < 0:
          return await m.reply(negate_group_text)
      if sudo:
        if user_id not in SUDO_USERS:
          return
      if owner:
        if user_id != OWNER_ID:
          return
      while True:
        try:
          await func(_, m, user)
          break
        except AttributeError:
          user = await load_attr(user_id)
        except Exception as e:
          import traceback
          tb = traceback.format_exc()
          await m.reply(f'Error: {e} at function: {func.__name__}, line: {tb.splitlines()[-2]}')
          break
    return wrapper
  return fun
