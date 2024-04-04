from pyrogram import Client
from ..Database.users import get_user
from ..Utils.markups import gender_markup, xprofile_markuo
from ..Utils.templates import xprofile_template

@Client.on_callback_query()
async def cbq(_, q):
  data, actual = q.data.split("_")
  actual = int(actual)
  if actual != q.from_user.id:
    return await q.answer()
  u = await get_user(q.from_user.id)
  if data == "gender":
    await q.answer()
    await q.edit_message_reply_markup(reply_markup=gender_markup(u))
  elif data == "male":
    if u.gender != 1:
      u.gender = 1
      await q.answer()
      await q.edit_message_text(xprofile_template(u), reply_markup=xprofile_markup(u))
      await u.update()
    else:
      await q.answer()
      await q.edit_message_reply_markup(reply_markup=xprofile_markup(u))
  elif data == "female":
    if u.gender != -1:
      u.gender = -1
      await q.answer()
      await q.edit_message_text(xprofile_template(u), reply_markup=xprofile_markup(u))
      await u.update()
    else:
      await q.answer()
      await q.edit_message_reply_markup(reply_markup=xprofile_markup(u))
  elif data == "other":
    if u.gender != 0:
      u.gender = 0
      await q.answer()
      await q.edit_message_text(xprofile_template(u), reply_markup=xprofile_markup(u))
      await u.update()
    else:
      await q.answer()
      await q.edit_message_reply_markup(reply_markup=xprofile_markup(u))
