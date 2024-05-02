from pyrogram import Client, filters
from . import YxH
from ..Utils.templates import xprofile_template
from ..Utils.markups import xprofile_markup

@Client.on_message(filters.command("xprofile")& ~filters.private)
@YxH())

async def xprofile(_, m, u):
  await m.reply(
    xprofile_template(u),
    reply_markup=xprofile_markup(u)
  )
