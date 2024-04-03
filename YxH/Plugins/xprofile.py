from . import Client, filters, YxH
from ..Utils.templates import xprofile_template

@Client.on_message(filters.command("xprofile"))
@YxH()
async def xprofile(_, m, u):
  await m.reply(xprofile_template(u))
