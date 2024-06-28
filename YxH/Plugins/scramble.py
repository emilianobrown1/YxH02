import random
from pyrogram import Client, filters
from . import YxH
from ..Database.users import get_user
from datetime import datetime, timedelta
import asyncio
from .word_pairs import word_pairs

active_scrambles = {}

@Client.on_message(filters.command('scramble'))
@YxH(private=False)
async def scramble(client, message, user):
    user_id = message.from_user.id

    if user_id in active_scrambles:
        return await message.reply("You are already playing the word scramble game!")

    user = await get_user(user_id)
    today = datetime.now().strftime("%Y-%m-%d")

    if user.scramble_completion.get(today, False):
        return await message.reply("You've already completed today's challenge. Come back tomorrow!")

    if user.scramble_progress.get('blocked_until') and datetime.now() < user.scramble_progress['blocked_until']:
        block_time_left = user.scramble_progress['blocked_until'] - datetime.now()
        return await message.reply(f"You are blocked from playing for another {block_time_left.seconds // 60} minutes.")

    if user.scramble_progress.get('incorrect_attempts') is None:
        user.scramble_progress['incorrect_attempts'] = 0
    if user.scramble_progress.get('stops') is None:
        user.scramble_progress['stops'] = 0
    if user.scramble_progress.get('skips') is None:
        user.scramble_progress['skips'] = 0
    if user.scramble_progress.get('count') is None:
        user.scramble_progress['count'] = 0
    if user.scramble_progress.get('completed') is None:
        user.scramble_progress['completed'] = False

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

def generate_hint(word, attempts):
    length = len(word)
    if length <= 2:
        return word
    middle_indices = [i for i in range(1, length - 1)]
    random.shuffle(middle_indices)
    middle_indices = sorted(middle_indices[:attempts])
    hint = (
        f"{word[0]}"
        f"{'_' * (middle_indices[0] - 1)}{word[middle_indices[0]]}"
        f"{'_' * (middle_indices[1] - middle_indices[0] - 1)}{word[middle_indices[1]]}"
        f"{'_' * (length - middle_indices[1] - 1)}{word[-1]}"
    )
    return hint

@Client.on_message(filters.text & filters.private)
async def catch_scramble_response(client, message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    today = datetime.now().strftime("%Y-%m-%d")

    if user_id in active_scrambles:
        scramble_data = active_scrambles[user_id]
        original_word = scramble_data['word']
        user_answer = message.text.strip().lower()

        if user_answer == "stop":
            user.scramble_progress['stops'] += 1
            if user.scramble_progress['stops'] > 2:
                await message.reply("You have stopped the game too many times. You cannot play for the next 3 hours.")
                user.scramble_progress['blocked_until'] = datetime.now() + timedelta(hours=3)
                active_scrambles.pop(user_id, None)
                await user.update()
                return
            await message.reply("🚫 **Game Stopped.** 🚫\n\nThank you for playing!")
            active_scrambles.pop(user_id, None)
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
                user.scramble_progress['completed'] = True
                user.scramble_completion[today] = True
                await user.update()
                await message.reply("🏆 **Congratulations!** 🏆\n\nYou've completed today's challenge and earned 8 crystals! 💎💎💎💎💎💎💎💎")
                active_scrambles.pop(user_id, None)
                return

            word, scrambled_word = random.choice(word_pairs)
            active_scrambles[user_id]['word'] = word
            active_scrambles[user_id]['attempts'] = 0
            await message.reply(f"Next word:\n\n**{scrambled_word}**\n\n⏳ *You have 30 seconds to respond.*")
        else:
            active_scrambles[user_id]['attempts'] += 1
            user.scramble_progress['incorrect_attempts'] += 1

            if active_scrambles[user_id]['attempts'] >= 3:
                await message.reply(f"❌ **Incorrect Answer!** ❌\n\nThe correct word was: **{original_word}**")
                active_scrambles.pop(user_id, None)
                if user.scramble_progress['incorrect_attempts'] >= 3:
                    user.scramble_progress['blocked_until'] = datetime.now() + timedelta(minutes=3)
                    await message.reply("You have failed too many times. You cannot play for the next 3 minutes.")
            else:
                attempts = active_scrambles[user_id]['attempts']
                hint = generate_hint(original_word, attempts)
                await message.reply(f"❌ **Incorrect Answer!** ❌\n\nHint: **{hint}**\n\nTry again.")

    await user.update()
