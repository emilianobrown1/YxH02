from pyrogram import Client, filters
from ..Database.users import get_user
from . import YxH

@Client.on_message(filters.command("invite"))
@YxH(private=False)
async def invite(_, m, u):
    if not user.invite_link:
        invite_link = await client.create_chat_invite_link(chat_id=message.chat.id, member_limit=1)
        user.invite_link = invite_link.invite_link
        await user.update()

    await message.reply(f"Share this link to invite friends and earn crystals: {user.invite_link}")

@Client.on_message(filters.new_chat_members)
async def handle_new_member(client, message):
    for member in message.new_chat_members:
        if message.invite_link:
            inviter_id = message.invite_link.inviter_id
            inviter = await User.get_user_by_id(inviter_id)

            if inviter:
                inviter.crystals += 50
                await inviter.update()

            new_user = await User.get_user_by_id(member.id)
            new_user.crystals += 100
            await new_user.update()

            await message.reply(
                f"{member.mention} joined using an invite link! "
                f"{inviter.user.mention} earned 50 crystals and {member.mention} earned 100 crystals."
            )
