from pyrogram import Client, filters
from . import YxH
from ..Utils.templates import xprofile_template
from ..Utils.markups import xprofile_markup

@Client.on_message(filters.command("xprofile"))
@YxH()
async def xprof(_, m, u):
  return await m.reply(
    await xprofile_template(u),
    reply_markup=xprofile_markup(u)
  )