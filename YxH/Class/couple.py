from ..Database.couple import add_couple, rmv_couple, get_couple

class Couple:
    def __init__(self, user_id):
        self.user_id = user_id

    async def add(self, partner_id: int):
        """Add a couple relationship."""
        await add_couple(self.user_id, partner_id)

    async def remove(self, partner_id: int):
        """Remove a couple relationship."""
        await rmv_couple(self.user_id, partner_id)

    async def get_partner(self):
        """Retrieve the user's partner."""
        return await get_couple(self.user_id)
