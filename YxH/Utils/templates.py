from ..Database.characters import get_anime_character

async def get_anime_image_and_caption(id: int) -> str:
  c = await get_anime_character(id)
  return c.image, "🎭 𝙉𝘼𝙈𝙀 : {}\n\n🎖𝘼𝙉𝙄𝙈𝙀 : {}\n\n💰 𝙋𝙍𝙄𝘾𝙀 : {} 💎\n\n♦️ {}\n\n🆔 : {}\n\n".format(c.name, c.anime, c.price, c.rarity, c.id)

def xprofile_template(user):
  return f'𝑼𝒔𝒆𝒓: {user.user.first_name}\n\n𝑮𝒆𝒏𝒅𝒆𝒓: {user.gl[user.gender]}\n\n𝑰𝑫: {user.user.id}\n𝑶𝒍𝒅: {user.get_old()}\n\n𝑪𝒓𝒚𝒔𝒕𝒂𝒍𝒔: {user.crystals} 🔮\n𝑮𝒆𝒎𝒔: {user.gems} 💎\n𝑮𝒐𝒍𝒅: {user.gold} 📯\n𝑻𝒓𝒆𝒂𝒔𝒖𝒓𝒆: {"Locked" if not user.treasure_state else "0, 0, 0"}\n\n𝑪𝒐𝒍𝒍𝒆𝒄𝒕𝒆𝒅 𝒄𝒉𝒂𝒓𝒂𝒄𝒕𝒆𝒓𝒔: {len(user.collection)}'


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
   txt = '🌈 New Character Alert: CATCH IT! 🌈''\n''Catch the Excitement!Join the adventure and add the newest member to your collection.Don`t miss out on the thrill of the chase!'
   txt += '\n\n'
   txt += f'🌻Anime: {info["anime"]}'
   txt += '\n'
   txt += f'💰Price: {info["price"]}'
   txt += '\n'
   txt += f'🎴ID: {info["id"]}'
   txt += '\n\n'
   txt += 'EXAMPLE - /copx [Character Name].'
   return txt

def inline_template(char):
   form = '🎭 Name : {}\n\n🎖 Anime : {}\n\n💰 Price : {} Gems\n\n♦️ : {}\n\n🆔 : {}'
   return form.format(
      char.name,
      char.anime,
      char.price,
      char.rarity,
      char.id
   )