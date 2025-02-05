from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ..Class.user import User
from ..Database.users import get_user
from ..Database.couples import add_couple, get_partner, remove_couple, get_all_couples, increment_couple_chat_messages
from .watchers import couple_watcher  

@Client.on_message(filters.command("propose") & filters.reply)
async def propose(client, message):
    sender = await get_user(message.from_user.id)
    receiver_user = message.reply_to_message.from_user

    # Prevent proposing to self
    if message.from_user.id == receiver_user.id:
        return await message.reply_text("You can't propose to yourself! 😢")

    receiver = await get_user(receiver_user.id)

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


@Client.on_message(filters.command("breakup"))
async def breakup(client, message):
    user = await get_user(message.from_user.id)

    if not user:
        return await message.reply_text("User not found in the database.")

    if not user.partner:
        return await message.reply_text("You are not in a relationship.")

    partner_id = user.partner
    partner = await get_user(partner_id)

    if partner:
        partner.partner = None
        await partner.update()

    user.partner = None
    await user.update()
    await remove_couple(user.user.id)

    await message.reply_text(f"You have broken up with {partner.user.first_name}. 💔")


@Client.on_message(filters.command("couples"))
async def show_couples(client, message):
    couples = await get_all_couples()
    
    if not couples:
        return await message.reply_text("There are no couples yet! 💔")

    response = "💖 **Couples in the Game** 💖\n\n"
    
    for index, (user1_id, user2_id) in enumerate(couples, start=1):
        user1 = await get_user(user1_id)
        user2 = await get_user(user2_id)
        
        if user1 and user2:
            response += f"{index}. {user1.user.first_name} ❤️ {user2.user.first_name}\n"

    await message.reply_text(response)


@Client.on_message(filters.text)  # Track non-command messages
async def handle_couple_messages(client, message):
    if not message.from_user:
        return

    sender_id = message.from_user.id
    chat_id = message.chat.id
    partner_id = await get_partner(sender_id)

    if not partner_id:
        return

    # Determine couple order (to avoid duplicates)
    user1 = min(sender_id, partner_id)
    user2 = max(sender_id, partner_id)

    try:
        count = await increment_couple_chat_messages(user1, user2, chat_id)
    except Exception as e:
        print(f"[ERROR] Failed to update couple chat count: {e}")
        return

    if count % 100 == 0:
        user1_obj = await get_user(user1)
        user2_obj = await get_user(user2)

        if user1_obj:
            await user1_obj.add_crystals(5)
        if user2_obj:
            await user2_obj.add_crystals(5)

        try:
            await message.reply_text(
                f"🎉 **Congratulations {user1_obj.user.first_name} and {user2_obj.user.first_name}!**\n"
                "You've sent 100 messages here! 💌\n"
                f"• {user1_obj.user.first_name} +5 🔮\n• {user2_obj.user.first_name} +5 🔮"
            )
        except Exception as e:
            print(f"[ERROR] Couldn't send congratulatory message: {e}")