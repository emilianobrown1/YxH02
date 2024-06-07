from pyrogram import Client, filters
from ..Class.clan import Clan
from ..Database.clan import get_clan, get_clans_count, get_clans
from ..Database.users import get_user
from ..universal_decorator import YxH
from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb
import random

temp = """
🏰 Clan Information 🏰

Clan: **{}**
Level: `{}`
Leader: **{}**
Members: `{}/15`

Join our mighty clan and conquer the fantasy world together! 💪🌟
"""

async def join_clan(_, m, user):
    id = int(m.text.split("_")[1])
    if user.clan_id:
        if user.clan_id == id:
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

@Client.on_message(filters.command("myclan"))
@YxH()
async def myc(_, m, u):
  if not u.clan_id:
    return await m.reply("You are not placed in any clan, You can join a clan or create one using /create.")
  clan = await get_clan(u.clan_id)
  markup = [[ikb("Members", callback_data=f"members_{u.user.id}")]]
  if u.user.id == clan.leader:
    markup.append([ikb("Settings", callback_data=f"settings_{u.user.id}")])
    markup.append([ikb(f"Requests ({len(clan.join_requests)})", callback_data=f"requests_{u.user.id}")])
  else:
    markup.append([ikb("Leave", callback_data=f"leave_{u.user.id}")])
  markup.append([ikb("Clan Link", url=f"https://t.me/{_.myself.username}?start=join_{clan.id}")])
  leader = await get_user(clan.leader)
  txt = temp.format(clan.name, clan.level, leader.user.first_name, len(clan.members)+1)
  return await m.reply(txt, reply_markup=ikm(markup))

@Client.on_message(filters.command("create"))
@YxH()
async def cr(_, m, u):
  if u.clan_id:
    return
  if len(m.text.split()) > 1:
    clan_name = "".join(m.text.split()[1:])
  else:
    return await m.reply("Usage: /create [clan name]")
  if u.crystals < 500:
    return await m.reply(f"You need `{500-u.crystals}` more crystal(s) to create a clan.")
  u.crystals -= 500
  clan_id = await get_clans_count() + 1
  u.clan_id = clan_id
  cl = Clan(clan_id, clan_name, u.user.id)
  ma = ikm([[ikb("Clan Link", url=f"https://t.me/{_.myself.username}?start=join_{clan_id}")]])
  await cl.update()
  await u.update()
  return await m.reply(f"(**{clan_name}**) Clan has been created.", reply_markup=ma)

def clans_markup(clans: list, user_id) -> ikm:
    lis = []
    def x(clan):
        return [ikb(clan.name, callback_data="answer"), ikb("View", callback_data=f"clan|{clan.id}_{user_id}")]
    for y in clans:
        lis.append(x(y))
    lis.append([ikb("Refresh", callback_data=f"refresh_{user_id}")])
    return ikm(lis)
    
@Client.on_message(filters.command("clans"))
@YxH()
async def clans(_, m, u):
    clans = await get_clans()
    clans = [x for x in clans if not x.private]
    new = random.sample(clans, 5)
    markup = clans_markup(new, u.user.id)
    await m.reply("**Here are some clans to join:**", reply_markup=markup)
    
def settings_markup(clan, user_id):
    lis = []
    lis.append([ikb("Approve Request", callback_data="answer"), ikb("❌" if clan.anyone_can_join else "✅", callback_data=f"togglejr_{user_id}")])
    lis.append([ikb("Visibility", callback_data="answer"), ikb("Private" if clan.private else "Public", callback_data=f"togglev_{user_id}")])
    lis.append([ikb("Back", callback_data=f"clanback_{user_id}")])
    return ikm(lis)
    
async def clanback_cbq(_, q, u):
  if not u.clan_id:
    return await q.answer("You are not placed in any clan, You can join a clan or create one using /create.", show_alert=True)
  clan = await get_clan(u.clan_id)
  markup = [[ikb("Members", callback_data=f"members_{u.user.id}")]]
  if u.user.id == clan.leader:
    markup.append([ikb("Settings", callback_data=f"settings_{u.user.id}")])
    markup.append([ikb(f"Requests ({len(clan.join_requests)})", callback_data=f"requests_{u.user.id}")])
  else:
    markup.append([ikb("Leave", callback_data=f"leave_{u.user.id}")])
  markup.append([ikb("Clan Link", url=f"https://t.me/{_.myself.username}?start=join_{clan.id}")])
  leader = u
  txt = temp.format(clan.name, clan.level, leader.user.first_name, len(clan.members)+1)
  await q.answer()
  return await q.edit_message_text(txt, reply_markup=ikm(markup))

async def settings_cbq(_, q, u):
    clan = await get_clan(u.clan_id)
    txt = "**Clan Settings:**"
    await q.answer()
    await q.edit_message_text(txt, reply_markup=settings_markup(clan, u.user.id))