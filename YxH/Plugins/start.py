from pyrogram import Client, filters
from ..Class import User
from ..Utils.strings import start_text
from ..Utils.markups import start_markup
from ..Database.users import get_user
from ..Database.clan import get_clan

@Client.on_message(filters.command("start") & filters.private)
async def start(_, m):
  user = await get_user(m.from_user.id)
  await m.reply_photo("Images/start.JPG", start_text.format(m.from_user.first_name), reply_markup=await start_markup())
  if not user:
    u = User(m.from_user)
    await u.update()
    
async def join_clan(_, m, user):
    if "join_" in m.text:
    id = int(m.text.split("_")[1])
    if user.clan_id:
        if user.clan_id = id:
            return await m.reply("You are already in the clan you want to join.")
        else:
            return await m.reply("You are already in a clan.")
    if user.crystals < 100:
        return await m.reply(f"You need `{100-user.crystals}` more crystal(s) to join.")
    clan = await get_clan(id)
    if clan.anyone_can_join:
        if len(clan.members) >= 15:
            return await m.reply("Clan is full!")
        user.clan_id = id
        user.crystals -= 100
        clan.members.append(m.from_user.id)
        await m.reply(f"You have joined **{clan.name}**.")
        await user.update()
        await clan.update()
    else:
        if m.from_user.id in clan.join_requests:
            return await m.reply("You have already requested to join.")
        clan.joun_requests.append(m.from_user.id)
        await m.reply("Requested to join.")
        await clan.update()
        