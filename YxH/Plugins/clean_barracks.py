# YxH/Plugins/clean_barracks.py
from pyrogram import filters
from pyrogram.types import Message
from ..Database.users import get_all_users
from ..universal_decorator import YxH
from config import OWNER_ID

@Client.on_message(filters.command("cleanbarracks") & filters.user(OWNER_ID))
@YxH()
async def barracks_cleaner(client: Client, message: Message):
    try:
        msg = await message.reply("🧹 Starting barracks data cleanup...")
        
        # Get all users
        all_users = await get_all_users()
        total_users = len(all_users)
        cleaned_count = 0
        
        # Clean attributes
        for idx, user in enumerate(all_users, 1):
            # Remove problematic attributes
            attrs_to_remove = ['barracks', 'barracks_manager', 'troops']
            for attr in attrs_to_remove:
                if hasattr(user, attr):
                    delattr(user, attr)
                    cleaned_count += 1
            
            # Save changes
            try:
                await user.update()
            except Exception as e:
                print(f"Error updating user {user.user.id}: {str(e)}")
            
            # Update progress every 50 users
            if idx % 50 == 0:
                await msg.edit_text(
                    f"🧼 Processing: {idx}/{total_users} users\n"
                    f"✅ Cleaned attributes: {cleaned_count}"
                )
        
        # Final message
        await msg.edit_text(
            f"🚨 Cleanup Complete!\n"
            f"• Total users processed: {total_users}\n"
            f"• Attributes removed: {cleaned_count}"
        )
        
    except Exception as e:
        await message.reply(f"❌ Cleanup failed: {str(e)}")
        raise e