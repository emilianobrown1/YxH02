import random
from pyrogram import Client, filters
from . import YxH
from ..Database.users import get_user
from datetime import datetime
import asyncio
from .word_pairs import word_pairs

active_scrambles = {}

@Client.on_message(filters.command('scramble'))
@YxH(private=False)
async def scramble(client, message, user):
    global active_scrambles
    user_id = message.from_user.id

    if user_id in active_scrambles:
        return await message.reply("You are already playing the word scramble game!")

    user = await get_user(user_id)

    intro_message = (
        f"🔠 **Welcome to Word Scramble!** 🔠\n\n"
        f"Can you unscramble this word? Try it out:"
    )

    word, scrambled_word = random.choice(word_pairs)

    active_scrambles[user_id] = {
        'word': word,
        'start_time': datetime.now(),
        'intro_message': intro_message,
        'attempts': 0,
        'correct_count': 0
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

        if user_answer == "stop":
            await message.reply("🚫 **Game Stopped.** 🚫\n\nThank you for playing!")
            active_scrambles.pop(user_id, None)
        elif user_answer == "skip":
            word, scrambled_word = random.choice(word_pairs)
            active_scrambles[user_id]['word'] = word
            active_scrambles[user_id]['attempts'] = 0
            await message.reply(f"⏭ **Word Skipped!** ⏭\n\nNext word:\n\n**{scrambled_word}**\n\n⏳ *You have 30 seconds to respond.*")
        elif user_answer == original_word:
            user = await get_user(user_id)

            scramble_data['correct_count'] += 1
            await message.reply(f"🎉 **Correct Answer!** 🎉\n\nYou've solved {scramble_data['correct_count']} words.")

            if scramble_data['correct_count'] % 10 == 0:
                user.crystals += 1
                await user.update()
                await message.reply("🏆 **Congratulations!** 🏆\n\nYou've earned 1 crystal! 🔮")

            word, scrambled_word = random.choice(word_pairs)
            active_scrambles[user_id]['word'] = word
            active_scrambles[user_id]['attempts'] = 0
            await message.reply(f"Next word:\n\n**{scrambled_word}**\n\n⏳ *You have 30 seconds to respond.*")
        else:
            active_scrambles[user_id]['attempts'] += 1
            if active_scrambles[user_id]['attempts'] >= 3:
                await message.reply(f"❌ **Incorrect Answer!** ❌\n\nThe correct word was: **{original_word}**")
                active_scrambles.pop(user_id, None)
            else:
                hint = f"{original_word[0]}{'_' * (len(original_word) - 2)}{original_word[-1]}"
                await message.reply(f"❌ **Incorrect Answer!** ❌\n\nHint: **{hint}**\n\nTry again.")

