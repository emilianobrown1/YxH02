from ..Database import db
from .user import User
import pickle

class Shift:
    def __init__(self, old_user_id: int, new_user_id: int):
        self.old_user_id = old_user_id
        self.new_user_id = new_user_id

    async def shift_user_data(self):
        # Fetch old and new user data
        old_user_data = await db.get_user(self.old_user_id)
        new_user_data = await db.get_user(self.new_user_id)

        if old_user_data and new_user_data:
            # Merge crystals, gems, and gold
            new_user_data.crystals += old_user_data.crystals
            new_user_data.gems += old_user_data.gems
            new_user_data.gold += old_user_data.gold

            # Merge collections
            new_user_data.collection.update(old_user_data.collection)

            # Merge inventory
            for item, count in old_user_data.inventory.items():
                new_user_data.inventory[item] += count

            # Merge other relevant fields (wordle, scramble, etc.)
            new_user_data.wordle.update(old_user_data.wordle)
            new_user_data.scramble.extend(old_user_data.scramble)

            # Save merged data for the new user
            new_user = User(self.new_user_id)
            await new_user.update()

            # Delete old user data
            await db.delete_user(self.old_user_id)

            return f"Successfully merged data from user {self.old_user_id} into user {self.new_user_id}."
        else:
            return "Either old user or new user not found."
