from pyrogram import Client, filters
from ..Database.users import get_all_users
from config import OWNER_ID

@Client.on_message(filters.command("nucleanclean") & filters.user(OWNER_ID))
async def nuclear_clean(client, message):
    try:
        msg = await message.reply("⚛️ Starting nuclear cleanup...")
        all_users = await get_all_users()
        
        barracks_attrs = [
            'barracks', 'barracks_manager', 'troops',
            'military_units', 'army', 'soldiers',
            'barracks_level', 'military', 'barracks_data'
        ]
        
        cleaned = 0
        for user in all_users:
            # Direct attribute removal
            for attr in barracks_attrs:
                try:
                    delattr(user, attr)
                except AttributeError:
                    continue
                cleaned += 1
            # Force save
            await user.update()
        
        await msg.edit_text(f"""
✅ Nuclear Cleanup Complete!
┣ Total Users: {len(all_users)}
┗ Removed Attributes: {cleaned}""")
        
    except Exception as e:
        await message.reply(f"💥 Failed: {str(e)}")
