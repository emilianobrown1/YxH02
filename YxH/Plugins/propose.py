from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ..Class.user import User
from ..Class.couple import Couple
from ..universal_decorator import YxH  # Importing the YxH decorator

@Client.on_message(filters.command("propose"))
@YxH()  # Adjusted function signature to align with YxH
async def propose_command(_, m: Message, u: User):
    if not m.reply_to_message:
        return await m.reply("❌ **You need to reply to someone's message to propose!**")

    proposer_id = m.from_user.id
    partner_id = m.reply_to_message.from_user.id

    if proposer_id == partner_id:
        return await m.reply("❌ **You cannot propose to yourself!**")

    proposer_couple = Couple(proposer_id)
    partner_couple = Couple(partner_id)

    # Check if either user is already in a couple
    if await proposer_couple.get_partner():
        return await m.reply("❌ **You are already in a relationship!**")
    if await partner_couple.get_partner():
        return await m.reply("❌ **The person you're proposing to is already in a relationship!**")

    # Send proposal message with inline buttons
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Yes 👩‍❤️‍👨", callback_data=f"accept_{proposer_id}_{partner_id}"),
                InlineKeyboardButton("No 🦵", callback_data=f"deny_{proposer_id}_{partner_id}")
            ]
        ]
    )
    await m.reply(
        f"💖 {m.reply_to_message.from_user.mention}, "
        f"{m.from_user.mention} is proposing to you! Will you accept?",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("^accept_"))
@YxH()  # Adjusted function signature for callback
async def accept_proposal(_, m: CallbackQuery, u: User):
    proposer_id, partner_id = map(int, m.data.split("_")[1:])

    # Validate that the correct user is clicking the button
    if m.from_user.id != partner_id:
        return await m.answer("❌ **This button is not for you!**", show_alert=True)

    proposer = Couple(proposer_id)
    partner = Couple(partner_id)

    # Try to add the couple relationship
    success = await proposer.add(partner_id)

    if not success:
        return await m.answer("❌ **One of you is already in a relationship!**", show_alert=True)

    # Notify both users
    await m.answer("✅ **Proposal accepted!**")
    await m.message.edit("🎉 **Congratulations! You are now a couple! 👩‍❤️‍👨**")
    try:
        await _.send_message(proposer_id, f"💖 **Your proposal was accepted by {m.from_user.mention}!**")
    except Exception:
        pass

@Client.on_callback_query(filters.regex("^deny_"))
@YxH()  # Adjusted function signature for callback
async def deny_proposal(_, m: CallbackQuery, u: User):
    proposer_id, partner_id = map(int, m.data.split("_")[1:])

    # Validate that the correct user is clicking the button
    if m.from_user.id != partner_id:
        return await m.answer("❌ **This button is not for you!**", show_alert=True)

    # Notify about the proposal rejection
    await m.answer("❌ **Proposal denied.**", show_alert=True)
    await m.message.edit("💔 **The proposal was denied. 🦵**")
    try:
        await _.send_message(proposer_id, f"❌ **Your proposal was denied by {m.from_user.mention}.**")
    except Exception:
        pass

@Client.on_message(filters.command("breakup"))
@YxH()  # Adjusted function signature for YxH
async def breakup_command(_, m: Message, u: User):
    user_id = m.from_user.id
    user_couple = Couple(user_id)

    partner_id = await user_couple.get_partner()
    if not partner_id:
        return await m.reply("❌ **You are not in a relationship!**")

    partner_couple = Couple(partner_id)

    # Remove the couple relationship
    await user_couple.remove()
    await partner_couple.remove()

    # Notify both users about the breakup
    await m.reply(f"💔 **You have broken up with {partner_id}. 😢**")
    try:
        await _.send_message(partner_id, f"💔 **{m.from_user.mention} has broken up with you. 😢**")
    except Exception:
        pass
