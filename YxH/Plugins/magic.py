from pyrogram import Client, filters
from . import YxH
from ..Database.users import get_user
from ..Class.user import User
from ..Database.characters import get_anime_character_ids
import time
import random

@Client.on_message(filters.command("magic"))
@YxH(private=False)
async def get_magic_item(client, message, user):
    # No need to fetch user again; user is already passed by YxH decorator
    
    # Check cooldown period
    current_time = time.time()
    if user.magic_uses > 0 and user.magic_uses % 2 == 0:
        if current_time - user.last_magic_use_time < 300:  # 5 minutes cooldown
            remaining_time = 300 - (current_time - user.last_magic_use_time)
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            await message.reply(f"Cooldown active. Please wait {minutes} minutes and {seconds} seconds before using the magic command again.")
            return

    if user.gold < 25000:
        await message.reply("You don't have enough gold! You need 25,000 gold to get a magic item.")
        return

    # Deduct 25,000 gold
    user.gold -= 25000

    # Randomly select a magic item
    items = ["Magic Key 🗝️", "Magic Diamond 💎", "Magic Potion 🧪", "Magic Stone 🪨"]
    selected_item = random.choice(items)
    user.inventory[selected_item] += 1

    # Update usage count and last use time
    user.magic_uses += 1
    user.last_magic_use_time = current_time
    await user.update()

    # Send the corresponding reply with an image
    if selected_item == "Magic Key 🗝️":
        await message.reply_photo("Images/key.jpg", caption="You received a Magic Key 🗝️!")
    elif selected_item == "Magic Diamond 💎":
        await message.reply_photo("Images/diamond.jpg", caption="You received a Magic Diamond 💎!")
    elif selected_item == "Magic Potion 🧪":
        await message.reply_photo("Images/potion.jpg", caption="You received a Magic Potion 🧪!")
    elif selected_item == "Magic Stone 🪨":
        await message.reply_photo("Images/stone.jpg", caption="You received a Magic Stone 🪨!")

    await message.reply(f"Congratulations! You received a {selected_item}.")

@Client.on_message(filters.command("inventory"))
@YxH(private=False)
async def show_inventory(client, message, user):
    # No need to fetch user again; user is already passed by YxH decorator

    inventory = "\n".join([f"{item}: {quantity}" for item, quantity in user.inventory.items()])
    await message.reply(f"Your inventory:\n{inventory}")

@Client.on_message(filters.command("use_magic"))
@YxH(private=False)
async def use_magic_item(client, message, user):
    # No need to fetch user again; user is already passed by YxH decorator

    command = message.text.split()
    if len(command) < 2:
        await message.reply("Please specify the magic item you want to use. (e.g., /use_magic Magic Key 🗝️)")
        return

    magic_item = " ".join(command[1:])
    if magic_item not in user.inventory or user.inventory[magic_item] <= 0:
        await message.reply(f"You don't have any {magic_item} in your inventory.")
        return

    # Logic to determine the rewards based on the quantity
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
