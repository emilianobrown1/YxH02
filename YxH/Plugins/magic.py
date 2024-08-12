from pyrogram import filters
from . import YxH
from class.user import User
import time
import random

@Client.on_message(filters.command("magic"))
async def get_magic_item(client, message,user):
    user = await User.get_user(message.from_user.id)

    if user is None:
        await message.reply("User data not found.")
        return

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

    # Deduct 15,000 gold
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
    if selected_item == "Magic Key":
        await message.reply_photo("Images/key.jpg", caption="You received a Magic Key 🗝️!")
    elif selected_item == "Magic Diamond":
        await message.reply_photo("Images/diamond.jpg", caption="You received a Magic Diamond 💎!")
    elif selected_item == "Magic Potion":
        await message.reply_photo("Images/Potion.jpg", caption="You received a Magic Potion 🧪!")
    elif selected_item == "Magic Stone":
        await message.reply_photo("Images/stone.jpg", caption="You received a Magic Stone 🪨!")

    await message.reply(f"Congratulations! You received a {selected_item}.")

@Client.on_message(filters.command("inventory"))
async def show_inventory(client, message, user):
    user = await User.get_user(message.from_user.id)

    if user is None:
        await message.reply("User data not found.")
        return

    inventory = "\n".join([f"{item}: {quantity}" for item, quantity in user.inventory.items()])
    await message.reply(f"Your inventory:\n{inventory}")

@Client.on_message(filters.command("use_magic"))
async def use_magic_item(client, message, user):
    user = await User.get_user(message.from_user.id)

    if user is None:
        await message.reply("User data not found.")
        return

    command = message.text.split()
    if len(command) < 2:
        await message.reply("Please specify the magic item you want to use. (e.g., /use_magic Magic Key)")
        return

    magic_item = " ".join(command[1:])
    if magic_item not in user.inventory or user.inventory[magic_item] <= 0:
        await message.reply(f"You don't have any {magic_item} in your inventory.")
        return

    # Use the magic item and provide the corresponding reward
    if magic_item == "Magic Key":
        user.gold += 100_000
    elif magic_item == "Magic Diamond":
        user.gems += 200_000
    elif magic_item == "Magic Potion":
        # Logic for using Magic Potion (spell) would go here
        await message.reply("You used a Magic Potion and sent a magical message to two characters!")
    elif magic_item == "Magic Stone":
        user.crystals += 10

    # Reduce the count of the used item in the inventory
    user.inventory[magic_item] -= 1
    await user.update()

    await message.reply(f"You used a {magic_item}. Your updated balance: {user.gold} gold, {user.gems} gems, {user.crystals} crystals.")
