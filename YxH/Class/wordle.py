from ..Database.wordle import db
import time
import pickle

class wordle:
    def __init__(self, user_id):
        self.user_id = user_id
        self.crystals = 0
        self.wordle_daily_limit = 20

    async def update(self):
        await db.users.update_one(
            {'user_id': self.user_id},
            {'$set': {'info': pickle.dumps(self)}},
            upsert=True
        )

    async def add_crystals(self, amount):
        self.crystals += amount
        await self.update()

    async def reset_wordle_daily_limit(self):
        self.wordle_daily_limit = 20
        await self.update()

    async def use_wordle_daily_limit(self):
        if self.wordle_daily_limit > 0:
            self.wordle_daily_limit -= 1
            await self.update()
            return True
        return False

    async def start_wordle_game(self, word):
        wordle_data = {
            "word": word,
            "guesses": [],
            "negated_letters": [],
            "start_time": time.time()
        }
        await db.wordle_games.update_one(
            {'user_id': self.user_id},
            {'$set': wordle_data},
            upsert=True
        )

    async def terminate_wordle_game(self):
        await db.wordle_games.delete_one({'user_id': self.user_id})

    async def get_wordle_game(self):
        game = await db.wordle_games.find_one({'user_id': self.user_id})
        return game

    async def add_wordle_guess(self, guess):
        game = await self.get_wordle_game()
        if game:
            guesses = game.get('guesses', [])
            guesses.append(guess)
            await db.wordle_games.update_one(
                {'user_id': self.user_id},
                {'$set': {'guesses': guesses}}
            )

    async def add_negated_letter(self, letter):
        game = await self.get_wordle_game()
        if game:
            negated_letters = game.get('negated_letters', [])
            negated_letters.append(letter)
            await db.wordle_games.update_one(
                {'user_id': self.user_id},
                {'$set': {'negated_letters': negated_letters}}
            )

    async def get_negated_letters(self):
        game = await self.get_wordle_game()
        if game:
            return game.get('negated_letters', [])
        return []

    async def get_wordle_word(self):
        game = await self.get_wordle_game()
        if game:
            return game.get('word')
        return None

    async def get_wordle_guesses(self):
        game = await self.get_wordle_game()
        if game:
            return game.get('guesses', [])
        return []