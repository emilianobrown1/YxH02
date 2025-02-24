from pyrogram import Client, filters
from ..Database.users import get_all_users
from ..universal_decorator import YxH
from config import OWNER_ID

@Client.on_message(filters.command("forceclean") & filters.user(OWNER_ID))
@YxH()
async def full_cleanup(client, message, u):
    try:
        msg = await message.reply("⚙️ Starting deep cleanup...")
        
        all_users = await get_all_users()
        total = len(all_users)
        cleaned = 0
        
        for user in all_users:
            # Force-update user to trigger __setstate__
            await user.update()
            cleaned += 1
            
            if cleaned % 50 == 0:
                await msg.edit_text(f"♻️ Processed {cleaned}/{total} users")
        
        await msg.edit_text(f"""
✅ **Full cleanup completed!**
┣ Total Users: `{total}`
┣ Cleaned Records: `{cleaned}`
┗ Database Restructured""")
        
    except Exception as e:
        await message.reply(f"❌ Failed: {str(e)}")