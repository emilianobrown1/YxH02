from pyrogram import Client, filters
from . import get_user, YxH
from ..Database.users import get_user
from pyrogram.types import Message


@Client.on_message(filters.command("propose"))
async def propose_handler(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("❌ **You need to reply to the person you want to propose to!**")

    proposer_id = message.from_user.id
    proposer = await get_user(proposer_id)

    if not proposer:
        return await message.reply("❌ **User not found in the database!**")

    # Check if the proposer is already in a relationship
    if await proposer.get_partner():
        return await message.reply("❌ **You are already in a relationship! Break up first to propose to someone else.**")

    proposed_id = message.reply_to_message.from_user.id
    if proposer_id == proposed_id:
        return await message.reply("❌ **You cannot propose to yourself!**")

    proposed = await get_user(proposed_id)
    if not proposed:
        return await message.reply("❌ **The person you are proposing to is not in the database!**")

    # Check if the proposed user is already in a relationship
    if await proposed.get_partner():
        return await message.reply("❌ **This person is already in a relationship!**")

    # Ask the proposed user to accept or reject the proposal
    buttons = [
        [
            ("💖 Accept", f"accept_proposal:{proposer_id}"),
            ("💔 Reject", f"reject_proposal:{proposer_id}")
        ]
    ]
    markup = InlineKeyboardMarkup(buttons)

    await message.reply_to_message.reply(
        f"💌 **{message.from_user.mention} has proposed to you! Will you accept?**",
        reply_markup=markup
    )
