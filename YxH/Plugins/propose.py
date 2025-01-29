from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ..class.user import User
from ..Database.users import get_user
from ..Database.couples import add_couple, get_partner

@Client.on_message(filters.command("propose") & filters.reply)
async def propose(client, message):
    sender = await get_user(message.from_user.id)
    receiver = await get_user(message.reply_to_message.from_user.id)

    if not sender or not receiver:
        return await message.reply_text("User not found in the database.")

    if sender.partner:
        return await message.reply_text("You are already in a relationship.")

    if receiver.partner:
        return await message.reply_text("This user is already in a relationship.")

    # Create inline buttons for Accept & Reject
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💍 Accept", callback_data=f"accept_{sender.user.id}")],
        [InlineKeyboardButton("❌ Reject", callback_data=f"reject_{sender.user.id}")]
    ])

    await message.reply_text(
        f"{receiver.user.first_name}, {sender.user.first_name} is proposing to you! ❤️\n"
        "Click a button to respond:",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("^accept_"))
async def accept_proposal(client, query: CallbackQuery):
    sender_id = int(query.data.split("_")[1])
    receiver_id = query.from_user.id

    sender = await get_user(sender_id)
    receiver = await get_user(receiver_id)

    if not sender or not receiver:
        return await query.answer("User data not found!", show_alert=True)

    if receiver.partner or sender.partner:
        return await query.answer("One of you is already in a relationship!", show_alert=True)

    sender.partner = receiver.user.id
    receiver.partner = sender.user.id
    await add_couple(sender.user.id, receiver.user.id)
    await sender.update()
    await receiver.update()

    await query.message.edit_text(f"💖 {sender.user.first_name} and {receiver.user.first_name} are now a couple! 💑")

@Client.on_callback_query(filters.regex("^reject_"))
async def reject_proposal(client, query: CallbackQuery):
    sender_id = int(query.data.split("_")[1])

    sender = await get_user(sender_id)
    if not sender:
        return await query.answer("User data not found!", show_alert=True)

    await query.message.edit_text("💔 Proposal rejected.")
