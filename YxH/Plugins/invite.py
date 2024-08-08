from pyrogram import Client, filters
from YxH.Class.user import User
import random

@Client.on_message(filters.command("invite"))
async def invite(client, message):
    user_id = message.from_user.id
    user = await User.get_user_by_id(user_id)  # Fetch the user from the database

    if not user.invite_link:  # Check if the user already has an invite link
        # Generate a unique invite link for the user
        invite_code = str(random.randint(100000, 999999))
        invite_link = f"https://t.me/YXH_GameBot?start={invite_code}"
        
        # Store the invite link in the user's data
        user.invite_link = invite_link
        await user.update()

        # Store the invite code mapping to the user ID in the database
        await store_invite_code(invite_code, user_id)
    else:
        invite_link = user.invite_link

    # Send the invite link to the user
    await message.reply(f"Here is your invite link: {invite_link}")

@Client.on_message(filters.regex(r'^/start (\d+)$'))
async def handle_invite(client, message):
    invite_code = message.matches[0].group(1)
    inviter_id = await find_inviter_by_code(invite_code)  # Implement this function to find the inviter by the code
    
    if inviter_id:
        inviter = await User.get_user_by_id(inviter_id)  # Fetch the inviter from the database
        invitee = User(message.from_user)  # New user who clicked the link

        # Award crystals
        inviter.crystals += 50
        invitee.crystals += 100

        # Update both users
        await inviter.update()
        await invitee.update()

        # Notify both users
        await client.send_message(inviter.user.id, "Congratulations! You've earned 50 crystals for inviting a new user.")
        await message.reply("Welcome! You've earned 100 crystals for joining via an invite link.")
    else:
        await message.reply("Invalid or expired invite link.")

async def store_invite_code(invite_code, user_id):
    # Implement this to store the invite code and the corresponding user ID in the database
    pass

async def find_inviter_by_code(invite_code):
    # Implement this to search the database for a user with the given invite code
    # Return the inviter's user ID if found, otherwise return None
    pass
