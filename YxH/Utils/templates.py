from ..Database.characters import get_anime_character

async def get_anime_image_and_caption(id: int) -> str:
  c = await get_anime_character(id)
  return c.image, "🎭 𝙉𝘼𝙈𝙀 : {}\n\n🎖𝘼𝙉𝙄𝙈𝙀 : {}\n\n💰 𝙋𝙍𝙄𝘾𝙀 : {} 💎\n\n♦️ {}\n\n🆔 : {}\n\n".format(c.name, c.anime, c.price, c.rarity, c.id)

def xprofile_template(user):
  return f'User: {user.user.first_name}\n\nGender: {user.gl[user.gender]}\n\nID: {user.user.id}\nOld: {user.get_old()}\n\nCrystals: {user.crystals} 🔮\nGems: {user.gems} 💎\nGold: {user.gold} 📯\nTreasure: {"Locked" if not user.treasure_state else "0, 0, 0"}\n\nCollected characters: {len(user.collection)}'

def acollection_template(lis: list[dict]) -> str:
    txt = ''
    for x in lis:
        txt += '🎭 𝙉𝘼𝙈𝙀 : ' + str(x.get('name', '')) + '\n\n'
        txt += '🎖𝘼𝙉𝙄𝙈𝙀 : ' + str(x.get('anime', '')) + '\n\n'
        txt += '💰 𝙋𝙍𝙄𝘾𝙀 : ' + str(x.get('price', '')) + '\n\n'
        txt += '♦️ Epic\n\n'
        txt += '🆔 : ' + str(x.get('id', '')) + '\n\n'
    return txt
