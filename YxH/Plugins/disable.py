from pyrogram import Client, filters
from ..Database.disabled import disable, enable
from config import SUDO_USERS
from . import YxH

@Client.on_message(filters.command('disable'))
@YxH(sudo=True)
async def dis(_, m, u):
  try:
    command = m.text.split()[1].lower()
  except:
    return
  await disable(command)
  await m.reply(f'Disabled `/{command}`.')

@Client.on_message(filters.command('enable'))
@YxH(sudo=True)
async def ena(_, m, u):
  try:
    command = m.text.split()[1].lower()
  except:
    return
  await enable(command)
  await m.reply(f'Enabled `/{command}`.')
