from ..Database.characters import get_anime_character
from ..Database.clan import get_clan

async def get_anime_image_and_caption(id: int) -> str:
  c = await get_anime_character(id)
  return c.image, "🎭 𝙉𝘼𝙈𝙀 : {}\n\n🎖𝘼𝙉𝙄𝙈𝙀 : {}\n\n💰 𝙋𝙍𝙄𝘾𝙀 : {} 💎\n\n♦️ {}\n\n🆔 : {}\n\n".format(c.name, c.anime, c.price, c.rarity, c.id)

async def xprofile_template(user):
  if user.clan_id:
      name = (await get_clan(user.clan_id)).name
  else:
      name = "-"
  return f'𝑼𝒔𝒆𝒓: {user.user.first_name}\n\nClan: {name}\n𝑮𝒆𝒏𝒅𝒆𝒓: {user.gl[user.gender]}\n\n𝑰𝑫: `{user.user.id}`\n𝑶𝒍𝒅: `{user.get_old()}` Day(s)\n\n𝑪𝒓𝒚𝒔𝒕𝒂𝒍𝒔: `{user.crystals}` 🔮\n𝑮𝒆𝒎𝒔: `{user.gems}` 💎\n𝑮𝒐𝒍𝒅: `{user.gold}` 📯\n𝑻𝒓𝒆𝒂𝒔𝒖𝒓𝒆: {"Locked" if not user.treasure_state else "0, 0, 0"}\n\n𝑪𝒐𝒍𝒍𝒆𝒄𝒕𝒆𝒅 𝒄𝒉𝒂𝒓𝒂𝒄𝒕𝒆𝒓𝒔: {len(user.collection)}'


def acollection_template(lis: list[dict], no: list[int]) -> str:
    txt = ''
    l = len(lis)
    for y in range(l):
        x = lis[y]
        o = no[y]
        txt += '🎭 𝙉𝘼𝙈𝙀 : ' + str(x.get('name', '')) + '\n'
        txt += '🎖 𝘼𝙉𝙄𝙈𝙀 : ' + str(x.get('anime', '')) + '\n'
        txt += '💰 𝙋𝙍𝙄𝘾𝙀 : ' + str(x.get('price', '')) + '\n'
        txt += '♦️ Epic\n'
        txt += '🆔 : ' + str(x.get('id', '')) + f' (x{o})' + '\n\n'
    return txt

def copx_template(info: dict) -> str:
   txt = '🌈 𝑵𝒆𝒘 𝑪𝒉𝒂𝒓𝒂𝒄𝒕𝒆𝒓 𝑨𝒍𝒆𝒓𝒕: 𝑪𝑨𝑻𝑪𝑯 𝑰𝑻! 🌈''\n''𝑪𝒂𝒕𝒄𝒉 𝒕𝒉𝒆 𝑬𝒙𝒄𝒊𝒕𝒆𝒎𝒆𝒏𝒕!𝑨𝒅𝒅 𝒕𝒉𝒆 𝒏𝒆𝒘𝒆𝒔𝒕 𝒎𝒆𝒎𝒃𝒆𝒓 𝒕𝒐 𝒚𝒐𝒖𝒓 𝒄𝒐𝒍𝒍𝒆𝒄𝒕𝒊𝒐𝒏.𝑫𝒐𝒏`𝒕 𝒎𝒊𝒔𝒔 𝒐𝒖𝒕 𝒐𝒏 𝒕𝒉𝒆 𝒕𝒉𝒓𝒊𝒍𝒍 𝒐𝒇 𝒕𝒉𝒆 𝒄𝒉𝒂𝒔𝒆!'
   txt += '\n\n'
   txt += f'🌻𝐀𝐧𝐢𝐦𝐞: {info["anime"]}'
   txt += '\n'
   txt += f'💰𝐏𝐫𝐢𝐜𝐞: {info["price"]}'
   txt += '\n'
   txt += f'🎴𝐈𝐃: {info["id"]}'
   txt += '\n\n'
   txt += 'ᴇxᴀᴍᴘʟᴇ - /ᴄᴏᴘx [ᴄʜᴀʀᴀᴄᴛᴇʀ ɴᴀᴍᴇ].'
   return txt

def inline_template(char):
   form = '🎭 Name : {}\n\n🎖 Anime : {}\n\n💰 Price : {} Gems\n\n♦️{}\n\n🆔 : {}'
   return form.format(
      char.name,
      char.anime,
      char.price,
      char.rarity,
      char.id
   )