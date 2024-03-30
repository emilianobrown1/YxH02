from ..Database.characters import get_character

async def get_image_and_caption(id):
  c = await get_character(id)
  cap = ""
  cap += f"Name: {c.name}\n"
  cap += f"{c.category}: {c.category_name}\n"
  cap += f"Price: {c.price}\n"
  cap += f"Rarity: {c.rarity}\n"
  cap += f"ID: {c.id}"
  return c.image, cap
