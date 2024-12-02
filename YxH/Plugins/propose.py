from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ..Database.couple import get_couple, get_top_couples, add_message_gems
from ..Class.user import User
from ..Class.couple import Couple

@Client.on_message(filters.command("propose"))
async def propose_command(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("❌ **You need to reply to someone's message to propose!**")

    proposer_id = message.from_user.id
    partner_id = message.reply_to_message.from_user.id

    if proposer_id == partner_id:
        return await message.reply("❌ **You cannot propose to yourself!**")

    proposer = User(proposer_id)
    partner = User(partner_id)

    proposer_couple = Couple(proposer_id)
    partner_couple = Couple(partner_id)

    # Check if either user is already in a couple
    if await proposer_couple.get_partner():
        return await message.reply("❌ **You are already in a relationship!**")
    if await partner_couple.get_partner():
        return await message.reply("❌ **The person you're proposing to is already in a relationship!**")

    # Send proposal message with inline buttons
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Yes 👩‍❤️‍👨", callback_data=f"accept_{proposer_id}_{partner_id}"),
                InlineKeyboardButton("No 🦵", callback_data=f"deny_{proposer_id}_{partner_id}")
            ]
        ]
    )
    await message.reply(
        f"💖 {message.reply_to_message.from_user.mention}, "
        f"{message.from_user.mention} is proposing to you! Will you accept?",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("^accept_"))
async def accept_proposal(client: Client, callback_query: CallbackQuery):
    _, proposer_id, partner_id = callback_query.data.split("_")
    proposer_id = int(proposer_id)
    partner_id = int(partner_id)

    # Validate that the correct user is clicking the button
    if callback_query.from_user.id != partner_id:
        return await callback_query.answer("❌ **This button is not for you!**", show_alert=True)

    proposer = Couple(proposer_id)
    partner = Couple(partner_id)

    # Try to add the couple relationship
    success = await proposer.add(partner_id)

    if not success:
        return await callback_query.answer("❌ **One of you is already in a relationship!**", show_alert=True)

    # Notify both users
    await callback_query.answer("✅ **Proposal accepted!**")
    await callback_query.message.edit("🎉 **Congratulations! You are now a couple! 👩‍❤️‍👨**")
    try:
        await client.send_message(proposer_id, f"💖 **Your proposal was accepted by {callback_query.from_user.mention}!**")
    except Exception:
        pass

@Client.on_callback_query(filters.regex("^deny_"))
async def deny_proposal(client: Client, callback_query: CallbackQuery):
    _, proposer_id, partner_id = callback_query.data.split("_")
    proposer_id = int(proposer_id)
    partner_id = int(partner_id)

    # Validate that the correct user is clicking the button
    if callback_query.from_user.id != partner_id:
        return await callback_query.answer("❌ **This button is not for you!**", show_alert=True)

    # Notify about the proposal rejection
    await callback_query.answer("❌ **Proposal denied.**", show_alert=True)
    await callback_query.message.edit("💔 **The proposal was denied. 🦵**")
    try:
        await client.send_message(proposer_id, f"❌ **Your proposal was denied by {callback_query.from_user.mention}.**")
    except Exception:
        pass

@Client.on_message(filters.command("breakup"))
async def breakup_command(client: Client, message: Message):
    user_id = message.from_user.id
    user_couple = Couple(user_id)

    # Retrieve the partner's user ID
    partner_id = await user_couple.get_partner()
    if not partner_id:
        return await message.reply("❌ **You are not in a relationship!**")

    partner_couple = Couple(partner_id)

    # Remove the couple relationship
    success = await user_couple.remove(partner_id)  # Pass partner_id
    if success:
        await partner_couple.remove(user_id)  # Pass user_id for the partner

        # Notify both users about the breakup
        await message.reply(f"💔 **You have broken up with {partner_id}. 😢**")
        try:
            await client.send_message(partner_id, f"💔 **{message.from_user.mention} has broken up with you. 😢**")
        except Exception:
            pass
    else:
        await message.reply("❌ **Failed to break up. Please try again later!**")


@Client.on_message(filters.command("top_couples"))
async def top_couples_handler(client, message):
    # Fetch the top couples
    top_couples = await get_top_couples(limit=10)

    # Build the leaderboard text
    leaderboard = "🏆 **Top Couples Leaderboard** 🏆\n\n"
    for idx, couple in enumerate(top_couples, start=1):
        user1 = couple["user1"]
        user2 = couple["user2"]
        gems = couple["message_gems"]
        leaderboard += f"{idx}. {user1} ❤️ {user2} - {gems} Gems\n"

    # Send the leaderboard
    await message.reply_text(leaderboard)
    
@Client.on_message(filters.command("check_couple"))
async def check_couple_handler(client: Client, message: Message):
    user_id = message.from_user.id
    couple = Couple(user_id)
    partner_id = await couple.get_partner()

    if partner_id:
        await message.reply(f"💞 **You are in a relationship with {partner_id}.**")
    else:
        await message.reply("❌ **You are not in a relationship.**")

@Client.on_message(filters.text & filters.command)
async def on_message(client: Client, message: Message):
    user_id = message.from_user.id

    # Fetch the user object
    user = User(user_id)

    # Check if the user has a couple
    couple_id = await user.get_partner()
    if couple_id:
        # Fetch the partner's User object
        couple_user = User(couple_id)

        # Reward gems
        user.gems += 10
        couple_user.gems += 10

        # Save updates to the database
        await user.update()
        await couple_user.update()

        # Track gems earned for leaderboard
        await add_message_gems(user_id, couple_id, 10)
