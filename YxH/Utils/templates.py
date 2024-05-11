from ..Database.characters import get_anime_character

async def get_anime_image_and_caption(id: int) -> str:
  c = await get_anime_character(id)
  return c.image, "🎭 𝙉𝘼𝙈𝙀 : {}\n\n🎖𝘼𝙉𝙄𝙈𝙀 : {}\n\n💰 𝙋𝙍𝙄𝘾𝙀 : {} 💎\n\n♦️ {}\n\n🆔 : {}\n\n".format(c.name, c.anime, c.price, c.rarity, c.id)

def xprofile_template(user):
  return f'User: {user.user.first_name}\n\nGender: {user.gl[user.gender]}\n\nID: {user.user.id}\nOld: {user.get_old()}\n\nCrystals: {user.crystals} 🔮\nGems: {user.gems} 💎\nGold: {user.gold} 📯\nTreasure: {"Locked" if not user.treasure_state else "0, 0, 0"}\n\nCollected characters: {len(user.collection)}'

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
