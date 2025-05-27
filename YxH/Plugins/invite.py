from pyrogram import Client, filters
from ..Class.user import User
from YxH.Database import db
import pickle

async def load_user_data(user_id):
    user_data = await db.users.find_one({'user_id': user_id})
    if user_data:
        return pickle.loads(user_data['info'])
    return None

@Client.on_message(filters.command("invite") & filters.private)
async def invite(_, m):
    user = await load_user_data(m.from_user.id)

    if user is None:
        user = User(m.from_user)
        await user.update()

    # Generate and show the user's invite link
    if not user.invite_link:
        user.invite_link = f"https://t.me/YXH_GameBot?start={m.from_user.id}"
        await user.update()

    await m.reply(f"Your invite link: {user.invite_link}")