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

    # Handle inviter reward (only once)
    if user.invited_by and not getattr(user, "invite_rewarded", False):
        inviter = await load_user_data(user.invited_by)
        if inviter:
            inviter.crystals += 20
            await inviter.update()

            # Mark user as rewarded
            user.invite_rewarded = True
            await user.update()

            # Notify inviter
            try:
                await _.send_message(
                    chat_id=inviter.user.id,
                    text=f"User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) joined using your invite link!\nYou received 20 crystals!"
                )
            except Exception as e:
                print(f"Failed to notify inviter: {e}")