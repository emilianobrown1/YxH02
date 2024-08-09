from pyrogram import Client, filters
from ..Class import User


@Client.on_message(filters.command("invite") & filters.private)
async def invite(_, m):
    user = await User.get_user(m.from_user.id)  # Assuming get_user is a method in the User class

    if not user.invite_link:
        invite_link = f"https://t.me/YXH_GameBot?start={m.from_user.id}"  # Replace with your bot username
        user.invite_link = invite_link
        await user.update()  # Update the user's data with the new invite link
        await m.reply(f"Share this link to invite others: {invite_link}")
    else:
        await m.reply(f"Your invite link: {user.invite_link}")

    # Reward the inviter
    if user.invited_by:
        inviter = await User.get_user(user.invited_by)
        if inviter:
            inviter.crystals += 50
            await inviter.update()  # Update the inviter's data with the new crystal count
            user.invited_by = None  # Reset the invited_by field after rewarding
            await user.update()  # Update the user's data with the reset invited_by field