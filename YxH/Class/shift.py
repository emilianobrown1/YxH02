# Class/shift.py
from ..Database.users import get_user, update_user

class Shift:
    def __init__(self, old_user_id: int, new_user_id: int):
        self.old_user_id = old_user_id
        self.new_user_id = new_user_id

    async def shift_user_data(self):
        old_user_data = await get_user(self.old_user_id)
        new_user_data = await get_user(self.new_user_id)

        if old_user_data and new_user_data:
            # Perform merge logic here (e.g., merging crystals, gems, collections, etc.)
            new_user_data.crystals += old_user_data.crystals
            new_user_data.gems += old_user_data.gems
            new_user_data.gold += old_user_data.gold

            # Example: merging collections
            new_user_data.collection.update(old_user_data.collection)

            # Save the merged new user data
            await update_user(self.new_user_id, new_user_data)

            # No deletion of the old user; it remains in the database
            return f"Data shifted from {self.old_user_id} to {self.new_user_id}."
        
        return "User not found."
