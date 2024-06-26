from pyrogram import Client, filters

@Client.on_message(filters.command('disable'))
@YxH(sudo=True)
async def dis(_, m, u):
  ...
