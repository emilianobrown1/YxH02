from pyrogram import Client, filters
from YxH.Class.user import User
import random

@Client.on_message(filters.command("invite"))
async def invite(client, message):
    user_id = message.from_user.id
    user = User(message.from_user)  # Assuming the User class is initialized this way

    # Generate a unique invite link for the user
    invite_code = str(random.randint(100000, 999999))  # Simple random code generation
    invite_link = f"https://t.me/YourBotName?start={invite_code}"

    # Store the invite link in the user's data (you can adjust this part)
    user.invite_link = invite_link
    await user.update()

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
        await client.send_message(inviter.user.id, f"Congratulations! You've earned 50 crystals for inviting a new user.")
        await message.reply(f"Welcome! You've earned 100 crystals for joining via an invite link.")
    else:
        await message.reply("Invalid or expired invite link.")

async def find_inviter_by_code(invite_code):
    # Implement this to search the database for a user with the given invite code
    # Return the inviter's user ID if found, otherwise return None
    pass
