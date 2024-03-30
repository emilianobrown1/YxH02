from ..Database.characters import get_anime_character

async def get_anime_image_and_caption(id: int) -> str:
  c = await get_anime_character(id)
  cap = "🎭 𝙉𝘼𝙈𝙀 : {}\n\n🎖𝘼𝙉𝙄𝙈𝙀 : {}\n\n💰 𝙋𝙍𝙄𝘾𝙀 : {} 💎\n\n🆔 : {}".format(c.name, c.anime, c.price, c.id)
  return cap