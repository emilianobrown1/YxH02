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

    if not user.invite_link:
        invite_link = f"https://t.me/YXH_GameBot?start={m.from_user.id}"
        user.invite_link = invite_link
        await user.update()
        await m.reply(f"Share this link to invite others: {invite_link}")
    else:
        await m.reply(f"Your invite link: {user.invite_link}")

    # Reward the inviter only once and notify them
    if user.invited_by and not getattr(user, "invite_rewarded", False):
        inviter = await load_user_data(user.invited_by)
        if inviter:
            inviter.crystals += 20
            await inviter.update()

            user.invite_rewarded = True
            await user.update()

            try:
                await _.send_message(
                    chat_id=inviter.id,
                    text=f"User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) joined using your invite link!\nYou've received 20 crystals."
                )
            except Exception as e:
                print(f"Failed to notify inviter: {e}")

            await m.reply("Your inviter has been rewarded with 20 crystals!")