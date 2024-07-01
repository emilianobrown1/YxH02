
import random
from pyrogram import Client, filters
from . import YxH
from ..Database.users import get_user
from datetime import datetime
import asyncio
from .word_pairs import word_pairs

active_scrambles = {}

def generate_hint(word):
    if len(word) <= 2:
        return word  # Not much to hint at if the word is very short
    middle_indices = list(range(1, len(word) - 1))
    if len(middle_indices) < 2:
        return word[0] + '_' * (len(word) - 2) + word[-1]
    random.shuffle(middle_indices)
    return (
        f"{word[0]}"
        f"{'_' * (middle_indices[0] - 1)}{word[middle_indices[0]]}"
        f"{'_' * (middle_indices[1] - middle_indices[0] - 1)}{word[middle_indices[1]]}"
        f"{'_' * (len(word) - middle_indices[1] - 1)}{word[-1]}"
    )

@Client.on_message(filters.command('scramble'))
@YxH(private=False)
async def scramble(client, message, user):
    user_id = message.from_user.id

    user = await get_user(user_id)
    today = datetime.now().strftime("%Y-%m-%d")

    if today in user.scramble:
        return await message.reply("You've already completed today's challenge. Come back tomorrow!")

    if user_id in active_scrambles:
        return await message.reply("You are already playing the word scramble game!")

    intro_message = (
        f"🔠 **Welcome to Word Scramble!** 🔠\n\n"
        f"Can you unscramble this word? Try it out:"
    )

    word, scrambled_word = random.choice(word_pairs)

    active_scrambles[user_id] = {
        'word': word,
        'start_time': datetime.now(),
        'intro_message': intro_message,
        'attempts': 0
    }

    await message.reply(f"{intro_message}\n\n**{scrambled_word}**\n\n⏳ *You have 30 seconds to respond.*")

    await asyncio.sleep(30)

    if user_id in active_scrambles and active_scrambles[user_id]['word'] == word:
        await message.reply("⏳ **Time's up!** ⏳\n\nPlease respond quicker next time.")
        active_scrambles.pop(user_id, None)


async def catch_scramble_response(client, message):
    user_id = message.from_user.id

    if user_id in active_scrambles:
        scramble_data = active_scrambles[user_id]
        original_word = scramble_data['word']
        user_answer = message.text.strip().lower()

        user = await get_user(user_id)

        if user_answer == "stop":
            await message.reply("🚫 **Game Stopped.** 🚫\n\nThank you for playing!")
            active_scrambles.pop(user_id, None)
            return

        elif user_answer == "skip":
            word, scrambled_word = random.choice(word_pairs)
            active_scrambles[user_id]['word'] = word
            active_scrambles[user_id]['attempts'] = 0
            await message.reply(f"⏭ **Word Skipped!** ⏭\n\nNext word:\n\n**{scrambled_word}**\n\n⏳ *You have 30 seconds to respond.*")

        elif user_answer == original_word:
            await message.reply("🎉 **Correct Answer!** 🎉\n\nYou've solved the word scramble challenge!")

            if today not in user.scramble:
                user.scramble.append(today)
                await user.update()
            active_scrambles.pop(user_id, None)
        else:
            active_scrambles[user_id]['attempts'] += 1
            if active_scrambles[user_id]['attempts'] >= 3:
                await message.reply(f"❌ **Incorrect Answer!** ❌\n\nThe correct word was: **{original_word}**")
                active_scrambles.pop(user_id, None)
            else:
                hint = generate_hint(original_word)
                await message.reply(f"❌ **Incorrect Answer!** ❌\n\nHint: **{hint}**\n\nTry again.")