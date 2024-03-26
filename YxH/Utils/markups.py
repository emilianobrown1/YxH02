from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb
from . import bot_info
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
