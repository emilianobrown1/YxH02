from pyrogram import Client, filters
from ..Class import User
from ..Database.users import get_user

GROUP_CHAT_ID = -1002014537230  # Replace with your group's chat ID

@Client.on_message(filters.command("invite") & filters.private)
async def invite(_, m):
    user = await get_user(m.from_user.id)
    
    if not user.invite_link:
        # Provide instructions for inviting the bot
        invite_instruction = (
            "To invite me to your group, please use the following link:\n"
            "https://t.me/YXH_GameBot?startgroup=-1002014537230\n\n"
            "Replace `YourBotUsername` with my username and `YourGroupID` with your group's ID.\n\n"
            "After inviting me, let me know so I can assist you with adding users to your group."
        )
        await m.reply(invite_instruction)
        
        # Update the invite link without changing other user data
        user.invite_link = "https://t.me/YourBotUsername?startgroup=YourGroupID"  # Update with actual link
        await user.update()
    else:
        await m.reply(f"Your invite link: {user.invite_link}")

    # Handle rewards for users who have been invited
    if user.invited_by:
        inviter = await get_user(user.invited_by)
        if inviter:
            inviter.crystals += 50
            await inviter.update()
            user.invited_by = None  # Reset after rewarding
            await user.update()
