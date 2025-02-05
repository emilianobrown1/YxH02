from pyrogram import Client, filters
from ..Database.couples import couples_db, get_couple, get_partner
from ..Database.users import get_user

async def handle_couple_messages(client, message):
    try:
        # Ignore bot messages
        if message.from_user.is_bot:
            return

        user_id = message.from_user.id
        partner_id = await get_partner(user_id)
        if not partner_id:
            return  # No partner, exit

        # Fetch the couple document
        couple = await get_couple(user_id)
        if not couple:
            return

        # Atomically increment message count
        updated_couple = await couples_db.find_one_and_update(
            {"_id": couple["_id"]},
            {"$inc": {"message_count": 1}},
            return_document=True
        )
        new_count = updated_couple["message_count"]

        # Check if message count is a multiple of 100
        if new_count % 2 == 0:
            user = await get_user(user_id)
            partner = await get_user(partner_id)
            if user and partner:
                user.crystals += 5
                partner.crystals += 5
                await user.update()
                await partner.update()
                # Notify in the chat where the milestone was reached
                await message.reply_text(
                    f"💎 **Congratulations {user.user.first_name} and {partner.user.first_name}!**\n"
                    "You've sent 100 messages together and earned 5 crystals each!"
                )
    except Exception as e:
        print(f"Error in couple message handler: {e}")