from ..Database.couple import add_couple, rmv_couple, get_couple

class Couple:
    def __init__(self, user_id):
        self.user_id = user_id

    async def add(self, partner_id: int):
        """Add a couple relationship between self.user_id and partner_id."""
        try:
            # Add the couple relationship using the database function
            await add_couple(self.user_id, partner_id)
            return True  # Successfully added the couple
        except Exception as e:
            # Log error if there's an issue (You may want to use logging here)
            print(f"Error adding couple: {e}")
            return False  # Indicate failure to add couple

    async def remove(self, partner_id: int):
        """Remove a couple relationship between self.user_id and partner_id."""
        try:
            # Remove the couple relationship using the database function
            await rmv_couple(self.user_id, partner_id)
            return True  # Successfully removed the couple
        except Exception as e:
            # Log error if there's an issue (You may want to use logging here)
            print(f"Error removing couple: {e}")
            return False  # Indicate failure to remove couple

    async def get_partner(self):
        """Retrieve the partner for self.user_id."""
        try:
            # Get the partner using the database function
            partner_id = await get_couple(self.user_id)
            if partner_id:
                return partner_id  # Return the partner ID if found
            else:
                return None  # No partner found
        except Exception as e:
            # Log error if there's an issue (You may want to use logging here)
            print(f"Error retrieving partner: {e}")
            return None  # Indicate failure to get partner
