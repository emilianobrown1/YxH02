from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ..Class.user import User  # User class to manage user-related operations
from ..Class.couple import Couple  # Couple class to manage couple-related operations

@Client.on_message(filters.command("propose"))
async def propose_command(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply("You need to reply to someone's message to propose!")
        return
    
    proposer_id = message.from_user.id
    partner_id = message.reply_to_message.from_user.id

    # Initialize User and Couple instances
    proposer = User(proposer_id)
    partner = User(partner_id)

    proposer_couple = Couple(proposer_id)
    partner_couple = Couple(partner_id)

    # Check if either user is already in a couple
    if await proposer_couple.get_partner():
        await message.reply("You are already in a relationship!")
        return
    
    if await partner_couple.get_partner():
        await message.reply("The person you're proposing to is already in a relationship!")
        return

    # Send proposal message with inline buttons
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Yes 👩‍❤️‍👨", callback_data=f"accept_{proposer_id}"),
                InlineKeyboardButton("No 🦵", callback_data=f"deny_{proposer_id}")
            ]
        ]
    )
    await message.reply(
        f"{message.reply_to_message.from_user.mention}, {message.from_user.mention} is proposing to you! Will you accept?",
        reply_markup=keyboard
    )
    
@Client.on_callback_query(filters.regex("^accept_"))
async def accept_proposal(client, callback_query):
    proposer_id = int(callback_query.data.split("_")[1])
    partner_id = callback_query.from_user.id

    # Try to add the couple relationship
    success = await Couple(proposer_id).add(partner_id)

    if not success:
        await callback_query.answer("One of you is already in a relationship!")
        return

    await callback_query.answer("Proposal accepted!")
    await callback_query.message.edit("Congratulations! You are now a couple! 👩‍❤️‍👨")

@Client.on_callback_query(filters.regex("^deny_"))
async def deny_proposal(client: Client, callback_query: CallbackQuery):
    proposer_id = int(callback_query.data.split("_")[1])

    # Notify about the proposal rejection
    await callback_query.answer("Proposal denied.", show_alert=True)
    await callback_query.message.edit("The proposal was denied. 🦵")

@Client.on_message(filters.command("breakup"))
async def breakup_command(client: Client, message: Message):
    user_id = message.from_user.id
    user = User(user_id)

    partner_id = await user.get_partner()
    if not partner_id:
        await message.reply("You are not in a relationship!")
        return

    partner = User(partner_id)

    # Remove couple relationship
    await user.remove_couple(partner_id)

    # Notify both users about the breakup
    await message.reply(f"You have broken up with {partner_id}. 😢")
    try:
        await client.send_message(partner_id, f"{message.from_user.mention} has broken up with you. 😢")
    except Exception:
        pass
