import random
import asyncio
from pyrogram import Client, filters
from ..universal_decorator import YxH
from ..Database import wordle as wordle_db
from .wordle_image import make_secured_image  # Module for updating game images
import wordle_words                        
from ..Database.users import get_user


# Crystal rewards mapping: crystals awarded based on attempt number
ATTEMPT_REWARDS = {
    1: 10,
    2: 7,
    3: 5,
    4: 3,
    5: 1
}

# A global dictionary to maintain active Wordle game sessions for each user.
active_wordle_games = {}

@Client.on_message(filters.command("wordle"))
@YxH(private=True, group=True)  # Now works in both private and group chats.
async def start_wordle(client, m, user):
    """
    Handles the /wordle command to start a new game.
    - Selects a random secret word.
    - Updates game statistics such as game count.
    - Stores the active game session in a dictionary.
    """
    user_id = m.from_user.id

    if user_id in active_wordle_games:
        await m.reply(
            "You already have an active Wordle game. Please finish the current game or use /cancel_wordle to cancel it."
        )
        return

    # Select a random secret word (assumes wordle_words.words contains your list of words)
    secret_word = random.choice(wordle_words.words).lower()

    # Update game statistics in the database
    await wordle_db.add_game(user_id)
    await wordle_db.incr_game(user_id)

    # Initialize the active game session
    active_wordle_games[user_id] = {
        "secret_word": secret_word,
        "attempt": 1,
        "guesses": []
    }

    await m.reply(
        "Your Wordle game has started!\n"
        "Please enter a 5-letter word guess. You have 5 attempts.\n"
        "Send your guesses in this chat."
    )

# Remove the 'private' filter so that group messages are also processed.
@Client.on_message(filters.text)
async def process_wordle_guess(client, m):
    """
    Processes text messages as Wordle guesses. If the user has an active game session,
    their message is treated as a guess regardless of whether it's in a private or group chat.
    After updating the image with the current state, if the guess is correct, 
    a crystal reward is given; otherwise, the game continues or ends after 5 attempts.
    """
    user_id = m.from_user.id

    # If there is no active Wordle session, ignore the message
    if user_id not in active_wordle_games:
        return

    game = active_wordle_games[user_id]
    current_attempt = game["attempt"]
    guess = m.text.strip().lower()

    if len(guess) != 5:
        await m.reply("Please provide a valid 5-letter word.")
        return

    # Add the guess to the game state and update the image
    game["guesses"].append(guess)
    image_path = await make_secured_image(user_id, game["secret_word"], game["guesses"])
    await m.reply_photo(
        photo=image_path,
        caption=f"Result for Attempt {current_attempt}."
    )

    # If the guess is correct, reward the user with crystals
    if guess == game["secret_word"]:
        reward = ATTEMPT_REWARDS.get(current_attempt, 0)
        # Retrieve the User instance (from your class/User.py)
        user = await get_user(user_id)
        # Use the User method to add crystals
        await user.add_crystals(reward)
        # Record the attempt in the database (for averaging statistics, etc.)
        await wordle_db.add(user_id, current_attempt)
        await m.reply(
            f"Congratulations! You guessed the correct word in {current_attempt} attempt(s).\n"
            f"You have been awarded {reward} crystals."
        )
        # Remove the active game session
        del active_wordle_games[user_id]
        return
    else:
        # If the guess is incorrect, check if more attempts are available
        current_attempt += 1
        if current_attempt > 5:
            # End the game after maximum attempts
            await m.reply(f"Game over. The correct word was: {game['secret_word']}.")
            del active_wordle_games[user_id]
        else:
            game["attempt"] = current_attempt
            await m.reply("Incorrect guess. Please try again!")

@Client.on_message(filters.command("cancel_wordle"))
@YxH(private=True, group=True)  # Now works in group chats as well.
async def cancel_wordle(client, m, user):
    """
    Allows the user to cancel their active Wordle game.
    """
    user_id = m.from_user.id
    if user_id in active_wordle_games:
        del active_wordle_games[user_id]
        await m.reply("Your active Wordle game has been cancelled.")
    else:
        await m.reply("You do not have any active Wordle game.")

@Client.on_message(filters.command("wxtop"))
@YxH(group=True, private=True)
async def wordle_leaderboard(client, m, user):
    """Displays the top 10 users based on games, average guesses, and crystals."""
    from ..Database.wordle import get_wordle_dic, get_avg
    from ..Database.users import get_user

    data = await get_wordle_dic()

    # Handle empty or invalid data
    if not data or not isinstance(data, dict):
        await m.reply("Leaderboard data is unavailable or corrupted.")
        return

    leaderboard = []
    for uid_str, total_games in data.items():
        try:
            uid = int(uid_str)
            total = int(total_games)
        except ValueError:
            continue  # Skip invalid entries

        avg = await get_avg(uid) or 0  # Default value if no average
        user_obj = await get_user(uid)
        crystals = user_obj.crystals if user_obj else 0

        leaderboard.append((uid, total, avg, crystals))

    # Sort by: total games (desc), avg (asc), crystals (desc)
    leaderboard.sort(key=lambda x: (-x[1], x[2], -x[3]))

    text = "**🏆 Wordle Leaderboard**\n\n"
    for rank, (uid, total, avg, crystals) in enumerate(leaderboard[:10], start=1):
        try:
            user_info = await client.get_users(uid)
            name = user_info.first_name
        except Exception as e:
            name = f"User {uid}"
            print(f"Error fetching user info: {e}")  # Debug user info fetch

        text += (
            f"{rank}. [{name}](tg://user?id={uid}) - "
            f"Games: {total}, Avg: {avg:.2f}, Crystals: {crystals}\n"
        )

    await m.reply(text)