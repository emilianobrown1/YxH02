from pyrogram import Client, filters
from . import YxH
from ..Database.users import get_user
from ..Class.user import User
from ..Database.characters import get_anime_character_ids
import time
import random

@Client.on_message(filters.command("magic"))
@YxH(private=False)
async def magic(client, message, user):
    current_time = time.time()
    if user.magic_uses > 0 and user.magic_uses % 2 == 0:
        if current_time - user.last_magic_use_time < 300:  # 5 minutes cooldown
            remaining_time = 300 - (current_time - user.last_magic_use_time)
            minutes, seconds = divmod(int(remaining_time), 60)
            await message.reply(f"Cooldown active. Please wait {minutes} minutes and {seconds} seconds before using the magic command again.")
            return

    if user.gold < 25000:
        await message.reply("You don't have enough gold! You need 25,000 gold to get a magic item.")
        return

    user.gold -= 25000

    items = ["Magic Key 🗝️", "Magic Diamond 💎", "Magic Potion 🧪", "Magic Stone 🪨"]
    selected_item = random.choice(items)
    user.inventory[selected_item] = user.inventory.get(selected_item, 0) + 1

    user.magic_uses += 1
    user.last_magic_use_time = current_time
    await user.update()

    image_map = {
        "Magic Key 🗝️": "Images/key.jpg",
        "Magic Diamond 💎": "Images/diamond.jpg",
        "Magic Potion 🧪": "Images/Spell.jpg",
        "Magic Stone 🪨": "Images/stone.jpg"
    }

    await message.reply_photo(image_map[selected_item], caption=f"You received a {selected_item}!")
    await message.reply(f"Congratulations! You received a {selected_item}.")


@Client.on_message(filters.command("inventory"))
@YxH(private=False)
async def show_inventory(client, message, user):
    if not user.inventory:
        await message.reply("Your inventory is empty.")
        return

    inventory_str = "🧙 Your Inventory:\n\n"
    
    magic_items = []
    for item, quantity in user.inventory.items():
        if "Magic" in item:
            magic_items.append(f"  • {item}: {quantity}")
    
    if magic_items:
        inventory_str += "✨ Magic Items:\n"
        inventory_str += "\n".join(magic_items)
        inventory_str += "\n\n"
    
    total_items = sum(user.inventory.values())
    inventory_str += f"🧚 Total Magic Items: {total_items}"

    await message.reply(inventory_str)

@Client.on_message(filters.command("use_magic"))
@YxH(private=False)
async def use_magic_item(client, message, user):
    command = message.text.split()
    if len(command) < 2:
        await message.reply("Please specify the magic item you want to use. (e.g., /use_magic Magic Key 🗝️)")
        return

    magic_item = " ".join(command[1:])
    if magic_item not in user.inventory or user.inventory[magic_item] <= 0:
        await message.reply(f"You don't have any {magic_item} in your inventory.")
        return

    if magic_item == "Magic Key 🗝️":
        if user.inventory[magic_item] >= 5:
            user.gold += 1_000_000
            user.inventory[magic_item] -= 5
            await message.reply("You used 5 Magic Keys 🗝️ and earned 1,000,000 gold!")
        else:
            await message.reply("You need at least 5 Magic Keys 🗝️ to use them.")

    elif magic_item == "Magic Diamond 💎":
        if user.inventory[magic_item] >= 15:
            user.gems += 2_000_000
            user.inventory[magic_item] -= 15
            await message.reply("You used 15 Magic Diamonds 💎 and earned 2,000,000 gems!")
        else:
            await message.reply("You need at least 15 Magic Diamonds 💎 to use them.")

    elif magic_item == "Magic Potion 🧪":
        if user.inventory[magic_item] >= 10:
            character_ids = await get_anime_character_ids(2)
            user.collection.update(character_ids)
            user.inventory[magic_item] -= 10
            await message.reply("You used 10 Magic Potions 🧪 and received 2 new characters!")
        else:
            await message.reply("You need at least 10 Magic Potions 🧪 to use them.")

    elif magic_item == "Magic Stone 🪨":
        if user.inventory[magic_item] >= 20:
            user.crystals += 10
            user.inventory[magic_item] -= 20
            await message.reply("You used 20 Magic Stones 🪨 and earned 10 crystals!")
        else:
            await message.reply("You need at least 20 Magic Stones 🪨 to use them.")

    await user.update()
    await message.reply(f"Your updated balance: {user.gold} gold, {user.gems} gems, {user.crystals} crystals.")
