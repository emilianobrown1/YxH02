from . import ikm, ikb
from .. import bot_info
from config import SUPPORT_GROUP, SUPPORT_CHANNEL

async def start_markup():
  info = await bot_info()
  start_markup = ikm(
    [
      [
        ikb("Add me to your group", url=f"https://t.me/{info.username}?startgroup=True")
      ],
      [
        ikb("Group", url=f"https://t.me/{SUPPORT_GROUP}"),
        ikb("Channel", url=f"https://t.me/{SUPPORT_CHANNEL}")
      ]
    ]
  )
  return start_markup

def store_markup(user_id, page: int):
  p = '👈'
  n = '👉'
  dic = {1: [3, 2], 2: [1, 3], 3: [2, 1]}
  markup = ikm(
    [
      [
        ikb(p, callback_data=f"turn|{dic[page][0]}_{user_id}"),
        ikb("Buy 💎", callback_data=f"buy|{page}_{user_id}"),
        ikb(n, callback_data=f"turn|{dic[page][1]}_{user_id}")
      ],
      [
        ikb("Close 🗑️", callback_data=f"close_{user_id}")
      ]
    ]
  )
  return markup

def gender_markup(u):
  g = u.gender
  uff = u.gl
  uff[g] += " ☑️"
  return ikm(
    [
      [
        ikb(uff[1], callback_data=f"male_{u.user.id}"),
        ikb(uff[-1], callback_data=f"female_{u.user.id}")
      ],
      [
        ikb(uff[0], callback_data=f"other_{u.user.id}")
      ]
    ]
  )

def xprofile_markup(u):
  return ikm(
    [
      [
        ikb("Gender", callback_data=f"gender_{u.user.id}")
      ]
    ]
  )

def acollection_markup(prev: int, next: int, u):
  markup = ikm(
    [
      [
        ikb('<-', callback_data=f'acoll|{prev}_{u.user.id}'),
        ikb('->', callback_data=f'acoll|{next}_{u.user.id}')
      ],
      [
        ikb('Close', callback_data=f'close_{u.user.id}')
      ]
    ]
  )
  return markup
