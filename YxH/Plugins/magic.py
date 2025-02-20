from pyrogram import Client, filters
from . import YxH
from ..Database.users import get_user
from ..Class.user import User
from ..Database.characters import get_anime_character_ids
import time
import random

MAX_LIMITS = {
    "Magic Key 🗝️": 100,
    "Magic Diamond 💎": 100,
    "Magic Potion 🧪": 100,
    "Magic Stone 🪨": 100
}

@Client.on_message(filters.command("magic"))
@YxH(private=False)
async def magic(_, m, u):
    current_time = time.time()
    if u.magic_uses > 0 and u.magic_uses % 5 == 0:
        if current_time - u.last_magic_use_time < 300:  # 5 minutes cooldown
            remaining_time = 300 - (current_time - u.last_magic_use_time)
            minutes, seconds = divmod(int(remaining_time), 60)
            await m.reply(f"Cooldown active. Please wait {minutes} minutes and {seconds} seconds before using the magic command again.")
            return

    if u.gold < 25000:
        await m.reply("You don't have enough gold! You need 25,000 gold to get a magic item.")
        return

    items = ["Magic Key 🗝️", "Magic Diamond 💎", "Magic Potion 🧪", "Magic Stone 🪨"]
    selected_item = random.choice(items)

    # Check if adding exceeds the max limit
    if u.inventory.get(selected_item, 0) >= MAX_LIMITS[selected_item]:
        await m.reply(f"You already have the maximum limit of {MAX_LIMITS[selected_item]} {selected_item}.")
        return

    u.gold -= 25000
    u.inventory[selected_item] = min(u.inventory.get(selected_item, 0) + 1, MAX_LIMITS[selected_item])

    u.magic_uses += 1
    u.last_magic_use_time = current_time
    await u.update()

    image_map = {
        "Magic Key 🗝️": "Images/key.jpg",
        "Magic Diamond 💎": "Images/diamond.jpg",
        "Magic Potion 🧪": "Images/Spell.jpg",
        "Magic Stone 🪨": "Images/stone.jpg"
    }

    await m.reply_photo(image_map[selected_item], caption=f"Congratulations! You received a {selected_item}!")


@Client.on_message(filters.command("inventory"))
@YxH(private=False)
async def show_inventory(_, m, u):
    if not u.inventory:
        await m.reply("Your inventory is empty.")
        return

    inventory_str = "🧙 Your Inventory:\n\n"

    magic_items = []
    for item, quantity in u.inventory.items():
        if "Magic" in item:
            magic_items.append(f"  • {item}: {quantity}")

    if magic_items:
        inventory_str += "✨ Magic Items:\n"
        inventory_str += "\n".join(magic_items)
        inventory_str += "\n\n"

    total_items = sum(u.inventory.values())
    inventory_str += f"🧚 Total Magic Items: {total_items}"

    await m.reply(inventory_str)

@Client.on_message(filters.command("use_magic"))
@YxH(private=False)
async def use_magic_item(_, m, u):
    command = m.text.split()
    if len(command) < 2:
        await m.reply("Please specify the magic item you want to use. (e.g., /use_magic Magic Key 🗝️)")
        return

    magic_item = " ".join(command[1:])
    if magic_item not in u.inventory or u.inventory[magic_item] <= 0:
        await m.reply(f"You don't have any {magic_item} in your inventory.")
        return

    if magic_item == "Magic Key 🗝️":
        if u.inventory[magic_item] >= 5:
            u.gold += 1_000_000
            u.inventory[magic_item] -= 5
            await m.reply("You used 5 Magic Keys 🗝️ and earned 1,000,000 gold!")
        else:
            await m.reply("You need at least 5 Magic Keys 🗝️ to use them.")

    elif magic_item == "Magic Diamond 💎":
        if u.inventory[magic_item] >= 15:
            u.gems += 2_000_00
            u.inventory[magic_item] -= 15
            await m.reply("You used 15 Magic Diamonds 💎 and earned 2,000,00 gems!")
        else:
            await m.reply("You need at least 15 Magic Diamonds 💎 to use them.")

    elif magic_item == "Magic Potion 🧪":
        if u.inventory[magic_item] >= 30:
            character_ids = await get_anime_character_ids()  # Get all character IDs
            selected_characters = random.sample(character_ids, 2)  # Randomly select 2 characters
            
            obtained_characters = []  # To store obtained character IDs for the reply message
            for char in selected_characters:
                u.collection[char] = u.collection.get(char, 0) + 1  # Update collection with selected characters
                obtained_characters.append(char)
            
            u.inventory[magic_item] -= 30  # Deduct 10 Magic Potions
            
            # Create a reply message with the obtained character IDs
            char_ids_str = ", ".join(str(char) for char in obtained_characters)
            await m.reply(f"You used 30 Magic Potions 🧪 and received 2 new random characters with IDs: {char_ids_str}!")
        else:
            await m.reply("You need at least 30 Magic Potions 🧪 to use them.")
            
    elif magic_item == "Magic Stone 🪨":
        if u.inventory[magic_item] >= 20:
            u.crystals += 10
            u.inventory[magic_item] -= 20
            await m.reply("You used 20 Magic Stones 🪨 and earned 10 crystals!")
        else:
            await m.reply("You need at least 20 Magic Stones 🪨 to use them.")

    await u.update()
    await m.reply(f"Your updated balance: {u.gold} gold, {u.gems} gems, {u.crystals} crystals.")
