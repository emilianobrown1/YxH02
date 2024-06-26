import random
from pyrogram import Client, filters
from . import YxH  # Ensure this import is correct
from ..Database.users import get_user  # Ensure correct import
from datetime import datetime
import asyncio
from .word_pairs import word_pairs  # Import the word pairs

active_scrambles = {}
daily_progress = {}

@Client.on_message(filters.command('scramble'))
@YxH(private=False)  # Ensure this decorator checks if the game can be played
async def scramble(client, message, user):
    user_id = message.from_user.id

    if user_id in active_scrambles:
        return await message.reply("You are already playing the word scramble game!")

    # Load the user's data
    user = await get_user(user_id)

    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")

    # Check if the user has already completed today's challenge
    if user_id in daily_progress and daily_progress[user_id]['date'] == today and daily_progress[user_id]['completed']:
        return await message.reply("You've already completed today's challenge. Come back tomorrow!")

    # Initialize or update the user's daily progress
    if user_id not in daily_progress or daily_progress[user_id]['date'] != today:
        daily_progress[user_id] = {'date': today, 'count': 0, 'completed': False, 'skips': 0}

    # Present the attractive introduction for the first word
    intro_message = (
        f"🔠 **Welcome to Word Scramble!** 🔠\n\n"
        f"Can you unscramble this word? Try it out:"
    )

    # Select a random word pair
    word, scrambled_word = random.choice(word_pairs)

    # Store the original word for checking the answer later
    active_scrambles[user_id] = {
        'word': word,
        'start_time': datetime.now(),
        'intro_message': intro_message,
        'attempts': 0
    }

    # Present the scrambled word to the user
    await message.reply(f"{intro_message}\n\n**{scrambled_word}**\n\n⏳ *You have 30 seconds to respond.*")

    while daily_progress[user_id]['count'] < 20:
        try:
            response = await client.listen(message.chat.id, filters=filters.user(user_id), timeout=30)
            user_answer = response.text.strip().lower()

            if user_answer == "stop":
                await message.reply("🚫 **Game Stopped.** 🚫\n\nThank you for playing!")
                active_scrambles.pop(user_id, None)
                break
            elif user_answer == "skip":
                daily_progress[user_id]['skips'] += 1
                if daily_progress[user_id]['skips'] > 2:
                    if user.crystals > 0:
                        user.crystals -= 1
                        await user.update()
                        await message.reply("⏭ **Word Skipped!** ⏭\n\n1 crystal has been deducted.")
                    else:
                        await message.reply("❌ **You don't have enough crystals to skip!** ❌")
                        continue
                word, scrambled_word = random.choice(word_pairs)
                active_scrambles[user_id]['word'] = word
                active_scrambles[user_id]['attempts'] = 0
                await message.reply(f"⏭ **Word Skipped!** ⏭\n\nNext word:\n\n**{scrambled_word}**\n\n⏳ *You have 30 seconds to respond.*")
            elif user_answer == word:
                daily_progress[user_id]['count'] += 1
                await message.reply(f"🎉 **Correct Answer!** 🎉\n\nYou've solved {daily_progress[user_id]['count']} words today.")

                # Check if the user has completed the daily challenge
                if daily_progress[user_id]['count'] >= 20:
                    user.crystals += 8  # Reward the user with 8 crystals
                    daily_progress[user_id]['completed'] = True
                    await user.update()

                    await message.reply("🏆 **Congratulations!** 🏆\n\nYou've completed today's challenge and earned 8 crystals! 💎💎💎💎💎💎💎💎")
                    break  # Exit the loop upon completing 20 words

                # Select a new word pair for the next challenge
                word, scrambled_word = random.choice(word_pairs)
                active_scrambles[user_id]['word'] = word
                active_scrambles[user_id]['attempts'] = 0
                await message.reply(f"Next word:\n\n**{scrambled_word}**\n\n⏳ *You have 30 seconds to respond.*")

            else:
                active_scrambles[user_id]['attempts'] += 1
                if active_scrambles[user_id]['attempts'] >= 3:
                    await message.reply(f"❌ **Incorrect Answer!** ❌\n\nThe correct word was: **{word}**")
                    active_scrambles.pop(user_id, None)
                    break
                else:
                    hint = f"{word[0]}{'_' * (len(word) - 2)}{word[-1]}"
                    await message.reply(f"❌ **Incorrect Answer!** ❌\n\nHint: **{hint}**\n\nTry again.")

        except asyncio.TimeoutError:
            await message.reply("⏳ **Time's up!** ⏳\n\nPlease respond quicker next time.")
            active_scrambles.pop(user_id, None)
            break

    # Remove the scramble from active scrambles
    active_scrambles.pop(user_id, None)

@Client.on_message(filters.text & filters.group)
async def catch_scramble_response(client, message):
    user_id = message.from_user.id

    if user_id in active_scrambles:
        original_word = active_scrambles[user_id]['word']
        user_answer = message.text.strip().lower()

        if user_answer == "stop":
            await message.reply("🚫 **Game Stopped.** 🚫\n\nThank you for playing!")
            active_scrambles.pop(user_id, None)
        elif user_answer == "skip":
            daily_progress[user_id]['skips'] += 1
            if daily_progress[user_id]['skips'] > 2:
                user = await get_user(user_id)
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
            user = await get_user(user_id)

            # Get today's date
            today = datetime.now().strftime("%Y-%m-%d")

            # Initialize or update the user's daily progress
            if user_id not in daily_progress or daily_progress[user_id]['date'] != today:
                daily_progress[user_id] = {'date': today, 'count': 0, 'completed': False}

            daily_progress[user_id]['count'] += 1
            await message.reply(f"🎉 **Correct Answer!** 🎉\n\nYou've solved {daily_progress[user_id]['count']} words today.")

            # Check if the user has completed the daily challenge
            if daily_progress[user_id]['count'] >= 20:
                user.crystals += 8  # Reward the user with 8 crystals
                daily_progress[user_id]['completed'] = True
                await user.update()

                await message.reply("🏆 **Congratulations!** 🏆\n\nYou've completed today's challenge and earned 8 crystals! 💎💎💎💎💎💎💎💎")
                active_scrambles.pop(user_id, None)  # Exit the scramble and stop further words
                return  # Stop further execution

            # Select a new word pair for the next challenge
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
