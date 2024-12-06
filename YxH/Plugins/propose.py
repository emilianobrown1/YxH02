from pyrogram import Client, filters
from . import get_user, YxH
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ..Database.users import get_user

@Client.on_message(filters.command("propose"))
async def propose_handler(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("❌ **You need to reply to the person you want to propose to!**")

    proposer_id = message.from_user.id
    proposer = await get_user(proposer_id)

    if not proposer:
        return await message.reply("❌ **User not found in the database!**")

    if await proposer.get_partner():
        return await message.reply("❌ **You are already in a relationship! Break up first to propose to someone else.**")

    proposed_id = message.reply_to_message.from_user.id
    if proposer_id == proposed_id:
        return await message.reply("❌ **You cannot propose to yourself!**")

    proposed = await get_user(proposed_id)
    if not proposed:
        return await message.reply("❌ **The person you are proposing to is not in the database!**")

    if await proposed.get_partner():
        return await message.reply("❌ **This person is already in a relationship!**")

    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💍 Accept", callback_data=f"accept_{proposer_id}_{proposed_id}"),
            InlineKeyboardButton("❌ Decline", callback_data=f"deny_{proposer_id}_{proposed_id}")
        ]
    ])
    await message.reply_to_message.reply(
        f"💌 **{message.from_user.mention} has proposed to you!**\n"
        f"💍 **Do you accept their proposal?**",
        reply_markup=markup
    )


# Accept Proposal Callback
@Client.on_callback_query(filters.regex(r"accept_(\d+)_(\d+)"))
async def accept_proposal(client, callback_query):
    proposer_id = int(callback_query.matches[0].group(1))
    partner_id = int(callback_query.matches[0].group(2))

    proposer = await get_user(proposer_id)
    partner = await get_user(partner_id)

    if not proposer or not partner:
        return await callback_query.answer("❌ **One of the users is not in the database!**", show_alert=True)

    if await proposer.get_partner() or await partner.get_partner():
        return await callback_query.answer("❌ **One of you is already in a relationship!**", show_alert=True)

    await proposer.set_partner(partner_id)
    await partner.set_partner(proposer_id)

    await client.send_message(
        proposer_id,
        f"💖 **Congratulations! {callback_query.from_user.mention} has accepted your proposal.**"
    )
    await callback_query.message.edit("💖 **You are now in a relationship!**")


# Deny Proposal Callback
@Client.on_callback_query(filters.regex(r"deny_(\d+)_(\d+)"))
async def deny_proposal(client: Client, callback_query: CallbackQuery):
    _, proposer_id, partner_id = callback_query.data.split("_")
    proposer_id, partner_id = int(proposer_id), int(partner_id)

    if callback_query.from_user.id != partner_id:
        return await callback_query.answer("❌ **This button is not for you!**", show_alert=True)

    await callback_query.answer("❌ **Proposal denied.**", show_alert=True)
    await callback_query.message.edit("💔 **The proposal was denied.**")
    try:
        await client.send_message(proposer_id, f"❌ **Your proposal was denied by {callback_query.from_user.mention}.**")
    except Exception:
        pass


# Breakup Command
@Client.on_message(filters.command("breakup"))
async def breakup_handler(client: Client, message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)

    if not user:
        return await message.reply("❌ **User not found in the database!**")

    partner_id = await user.get