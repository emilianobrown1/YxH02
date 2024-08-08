from pyrogram import Client, filters
from ..Class import User
from . import YxH, get_user

@Client.on_message(filters.command("invite") & filters.private)
async def invite(_, m):
    user = await get_user(m.from_user.id)
    
    if not user.invite_link:
        # Generate an invite link for the user
        invite_link = f"https://t.me/YXH_GameBot?start={m.from_user.id}"  # Replace with your bot username
        await user.update_invite_link(invite_link)
        await m.reply(f"Share this link to invite others: {invite_link}")
    else:
        await m.reply(f"Your invite link: {user.invite_link}")

    # Reward the inviter
    if user.invited_by:
        inviter = await get_user(user.invited_by)
        if inviter:
            inviter.crystals += 50
            await inviter.update()
            user.invited_by = None  # Reset after rewarding
            await user.update()
