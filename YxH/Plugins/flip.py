import random
import asyncio
from pyrogram import Client, filters

@Client.on_message(filters.command("flipcoin"))
async def flip_coin(client, message):
    # Step 1: Show coin
    coin_msg = await message.reply("🪙")
    await asyncio.sleep(1.5)
    await coin_msg.delete()

    # Step 2: Suspense message
    suspense = await message.reply("🤞 Flipping the coin...")
    await asyncio.sleep(2)

    # Step 3: Randomly choose result
    result = random.choice(["heads", "tails"])

    # Step 4: Edit the suspense message
    await suspense.edit(f"🪙 The coin landed on {result}!")