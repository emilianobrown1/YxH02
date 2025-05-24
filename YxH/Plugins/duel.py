from pyrogram import Client, filters
from ..Database.users import get_user
from ..Class.duel import Duel, Arena
from ..Class.duel_state import active_duels, active_arenas
from ..Utils.duel_utils import get_duel_keyboard, format_arena_progress, get_duel_keyboard
import random

@Client.on_message(filters.command("duel") & filters.reply)
async def start_duel(client, message):
    from_user = message.from_user
    to_user = message.reply_to_message.from_user

    if from_user.id == to_user.id:  
        await message.reply("You cannot duel yourself!")  
        return  

    if from_user.id in active_duels or to_user.id in active_duels:  
        await message.reply("Either you or your opponent is already in a duel!")  
        return  

    u1 = await get_user(from_user.id)  
    u2 = await get_user(to_user.id)  

    cost = 100_000  
    if u1.gold < cost:  
        await message.reply("You don't have enough gold to duel! (Need 100,000 gold)")  
        return  
    if u2.gold < cost:  
        await message.reply("Your opponent doesn't have enough gold to duel! (Need 100,000 gold)")  
        return  

    try:  
        u1.gold -= cost  
        u2.gold -= cost  
        await u1.update()  
        await u2.update()  

        duel = Duel(u1.user.id, u2.user.id)  
        active_duels[u1.user.id] = duel  
        active_duels[u2.user.id] = duel  

        player1_char = duel.players[u1.user.id]['name']  
        player2_char = duel.players[u2.user.id]['name']  
        current_turn_char = duel.players[duel.turn]['name']  

        text = (  
            f"⚔️ Duel started between:\n"
            f"• {player1_char} ({from_user.first_name})\n"  
            f"• {player2_char} ({to_user.first_name})\n\n"  
            f"🎮 Current turn: {current_turn_char} ({duel.turn == from_user.id and from_user.first_name or to_user.first_name})"
        )  
        keyboard = get_duel_keyboard(u1.user.id, duel.players[u1.user.id]['abilities'])
        await message.reply(text, reply_markup=keyboard)  

    except Exception as e:  
        u1.gold += cost  
        u2.gold += cost  
        await u1.update()  
        await u2.update()  
        await message.reply(f"❌ Failed to start duel: {str(e)}")  
        active_duels.pop(u1.user.id, None)  
        active_duels.pop(u2.user.id, None)



@Client.on_message(filters.command("arena") & filters.reply)
async def start_arena(client, message):
    from_user = message.from_user
    to_user = message.reply_to_message.from_user
    entry_cost = 200000

    # Existing checks and balance validation
    u1 = await get_user(from_user.id)
    u2 = await get_user(to_user.id)

    if u1.gold < entry_cost or u2.gold < entry_cost:
        await message.reply("❌ Both players need 200,000 gold to enter the arena!")
        return

    # Deduct gold
    u1.gold -= entry_cost
    u2.gold -= entry_cost
    await u1.update()
    await u2.update()

    arena = Arena(from_user.id, to_user.id)
    active_arenas[from_user.id] = arena
    active_arenas[to_user.id] = arena

    # Start first round
    arena.start_next_round()
    
    text = format_arena_progress(arena)
    text += "\n\n⚔️ Round 1 Started!"
    text += f"\n{arena.get_round_characters()[0]} vs {arena.get_round_characters()[1]}"
    
    await message.reply(text, reply_markup=get_duel_keyboard(from_user.id, 
        arena.active_duel.players[from_user.id]['abilities']))