hi from .Database.users import get_user
from .Utils.force_start import force_start
from .Utils.strings import block_text, negate_private_text, negate_group_text
from config import SUDO_USERS, OWNER_ID, MAIN_GROUP_ID
from .load_attr import load_attr, load_clan_attr
import traceback

import aiohttp

async def download_image(url, save_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(save_path, 'wb') as f:
                    f.write(await response.read())

me = None

def YxH(
  private=True,
  group=True,
  sudo=False,
  owner=False,
  main_only=False,
  min_old=0
):
  def fun(func):
    async def wrapper(_, m, *args):
      global me
      if not me:
        me = await _.get_me()
      _.myself = me
      user_id = m.from_user.id
      chat_id = m.chat.id
      user = await get_user(user_id)
      
      # ---------
      x = m.reply_photo
      async def reply_image(url, *args, **kwargs):
        try:
          await x(url, *args, **kwargs)
        except:
          await download_image(url, "dl.jpg")
          await x("dl.jpg", *args, **kwargs)
      m.reply_photo = reply_image
      # ---------
      
      if not user:
        return await force_start(m)
      if user.blocked:
        return await m.reply(block_text)
      if main_only:
        if m.chat.id != MAIN_GROUP_ID:
          return await m.reply("**This command only works in maim group.**")
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
      if min_old > 0:
        if user.get_old() < min_old:
          return await m.reply(f"You must be atleast `{min_old}` day(s) old to use this command.")
      try:
        await func(_, m, user)
      except Exception as e:
        tb = traceback.format_exc()
        await m.reply(f'Error: {e} at function: {func.__name__}, line: {tb.splitlines()[-2]}')
    return wrapper
  return fun
