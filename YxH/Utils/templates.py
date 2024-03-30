from ..Database.characters import get_anime_character

async def get_anime_image_and_caption(id):
  c = await get_anime_character(id)
  cap = ""
  cap += f"Name: {c.name}\n\n"
  cap += f"Anime: {c.anime}\n\n"
  cap += f"Price: {c.price}\n\n"
  cap += f"Rarity: {c.rarity}\n\n"
  cap += f"ID: {c.id}"
  return c.image, cap