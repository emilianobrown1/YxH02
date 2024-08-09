from pyrogram import Client, filters
from ..Class.user import User
from YxH.Database import db
import pickle

async def load_user_data(user_id):
    # Load user data from the database
    user_data = await db.users.find_one({'user_id': user_id})
    if user_data:
        return pickle.loads(user_data['info'])
    return None

@Client.on_message(filters.command("invite") & filters.private)
async def invite(_, m):
    user = await load_user_data(m.from_user.id)  # Load the user data from the database

    if user is None:  # If the user doesn't exist in the database, create a new User instance
        user = User(m.from_user)
        await user.update()  # Save the new user to the database

    if not user.invite_link:
        invite_link = f"https://t.me/YXH_GameBot?start={m.from_user.id}"  # Replace with your bot's username
        user.invite_link = invite_link
        await user.update()  # Update the user's data with the new invite link
        await m.reply(f"Share this link to invite others: {invite_link}")
    else:
        await m.reply(f"Your invite link: {user.invite_link}")

    # Reward the inviter if the user was invited by someone
    if user.invited_by:
        inviter = await load_user_data(user.invited_by)  # Load the inviter's data from the database
        if inviter:
            inviter.crystals += 20
            await inviter.update()  # Update the inviter's data with the new crystal count
            # We're not clearing the invited_by field to preserve this information
            await m.reply(f"Your inviter has been rewarded with 20 crystals!")