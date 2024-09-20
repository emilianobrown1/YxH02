import random
from ..Database.characters import get_anime_character
from ..Database.users import get_user

@Client.on_message(filters.command("purchase"))
async def purchase_character(_, m):
    spl = m.text.split()
    if len(spl) < 2:
        await m.reply("Usage:\n\n`/purchase <character_id>`")
        return

    try:
        char_id = int(spl[1])  # Get the character ID from the command
    except ValueError:
        await m.reply("Please provide a valid character ID.")
        return

    # Fetch the user
    u = await get_user(m.from_user.id)

    # Fetch the anime character
    character = await get_anime_character(char_id)
    if not character:
        await m.reply("This character does not exist.")
        return

    # Determine the cost in crystals (random between 80 and 120)
    cost = random.randint(80, 120)

    # Check if the user has enough crystals
    if u.crystals < cost:
        await m.reply(f"You need {cost} crystals to purchase this character, but you only have {u.crystals}.")
        return

    # Deduct the crystals and add the character to the user's collection
    u.crystals -= cost
    u.collection[char_id] = u.collection.get(char_id, 0) + 1  # Add the character to the collection

    # Update the user in the database
    await u.update()

    # Reply with a success message
    await m.reply(f"Congratulations! You purchased the character with ID {char_id} for {cost} crystals.")