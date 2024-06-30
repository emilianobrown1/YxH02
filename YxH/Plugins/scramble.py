import random
from pyrogram import Client, filters
from . import YxH
from ..Database.users import get_user
from datetime import datetime, timedelta
import asyncio
from .word_pairs import word_pairs

active_scrambles = {}

def generate_hint(word, attempts):
    if len(word) <= 2:
        return word
    hint = ['_'] * len(word)
    hint[0] = word[0]
    hint[-1] = word[-1]
    reveal_count = min(attempts, len(word) - 2)
    for i in range(1, reveal_count + 1):
        hint[i] = word[i]
    return ''.join(hint)

@Client.on_message(filters.command('scramble'))
@YxH(private=False)
async def scramble(client, message, user):
    user_id = message.from_user.id
    user = await get_user(user_id)
    today = datetime.now().strftime("%Y-%m-%d")

    user.reset_daily_state()

    if user.scramble_completion.get(today, False):
        return await message.reply("You've already completed today's challenge. Come back tomorrow!")

    if user.scramble_progress.get('blocked_until') and datetime.now() < user.scramble_progress['blocked_until']:
        block_duration = user.scramble_progress['blocked_until'] - datetime.now()
        return await message.reply(f"You are blocked from playing for another {block_duration.seconds // 60} minutes.")
    else:
        user.scramble_progress['blocked_until'] = None
        await user.update()

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
            user.scramble_progress['stops'] += 1
            if user.scramble_progress['stops'] > 2:
                user.scramble_progress['blocked_until'] = datetime.now() + timedelta(hours=3)
                await user.update()
                await message.reply("🚫 **Game Stopped.** 🚫\n\nYou have stopped the game too many times and are blocked for 3 hours.")
            else:
                await message.reply("🚫 **Game Stopped.** 🚫\n\nThank you for playing!")
            active_scrambles.pop(user_id, None)
            return

        elif user_answer == "skip":
            user.scramble_progress['skips'] += 1
            if user.scramble_progress['skips'] > 2:
                if user.crystals > 0:
                    user.crystals -= 1
                    await user.update()
                    await message.reply("⏭ **Word Skipped!** ⏭\n\n1 crystal has been deducted.")
                else:
                    await message.reply("❌ **You don't have enough crystals to skip!** ❌")
                    return
            word, scrambled_word = random.choice(word_pairs)
            active_scrambles[user_id]['word'] = word
            active_scrambles[user_id]['attempts'] = 0
            await message.reply(f"⏭ **Word Skipped!** ⏭\n\nNext word:\n\n**{scrambled_word}**\n\n⏳ *You have 30 seconds to respond.*")

        elif user_answer == original_word:
            user.scramble_progress['count'] += 1
            await message.reply(f"🎉 **Correct Answer!** 🎉\n\nYou've solved {user.scramble_progress['count']} words today.")

            if user.scramble_progress['count'] >= 20:
                user.crystals += 8
                user.scramble_completion[today] = True
                user.scramble_progress['count'] = 0
                await user.update()
                await message.reply("🏆 **Congratulations!** 🏆\n\nYou've completed today's challenge and earned 8 crystals! 🔮🔮🔮🔮🔮🔮🔮🔮")
                active_scrambles.pop(user_id, None)
                return

            word, scrambled_word = random.choice(word_pairs)
            active_scrambles[user_id]['word'] = word
            active_scrambles[user_id]['attempts'] = 0
            await message.reply(f"Next word:\n\n**{scrambled_word}**\n\n⏳ *You have 30 seconds to respond.*")

        else:
            active_scrambles[user_id]['attempts'] += 1
            if active_scrambles[user_id]['attempts'] >= 3:
                user.scramble_progress['blocked_until'] = datetime.now() + timedelta(minutes=5)
                await user.update()
                await message.reply(f"❌ **Incorrect Answer!** ❌\n\nThe correct word was: **{original_word}**\nYou are blocked from playing for 5 minutes.")
                active_scrambles.pop(user_id, None)
            else:
                hint = generate_hint(original_word, active_scrambles[user_id]['attempts'])
                await message.reply(f"❌ **Incorrect Answer!** ❌\n\nHint: **{hint}**\n\nTry again.")
            await user.update()