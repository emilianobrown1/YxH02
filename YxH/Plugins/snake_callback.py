import time
import random
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup
from ..Utils.snake import snake_manager, create_snake_board
from ..Database.snake import add_snake_game
from ..Class.user import User

async def handle_snake_game(client, q: CallbackQuery):
    if not q.data.startswith("snake_"):
        return False

    parts = q.data.split('_')
    action = parts[1]
    chat_id = int(parts[2])
    game = snake_manager.games.get(chat_id)

    if not game:
        await q.answer("Game expired!", show_alert=True)
        return True

    user_id = q.from_user.id

    try:
        if action == "join":
            return await handle_join(client, q, game, user_id, chat_id)
        elif action == "dir":
            return await handle_move(q, game, user_id, parts[3], chat_id)
        elif action == "quit":
            return await handle_quit(client, q, game, chat_id)
        else:
            await q.answer("Use arrow buttons to move your snake!", show_alert=True)
            return True

    except Exception as e:
        print(f"Snake error: {e}")
        await q.answer("🐍 Game error!", show_alert=True)
        snake_manager.end_game(chat_id)
        return True

async def handle_join(client, q, game, user_id, chat_id):
    if game['status'] != 'waiting':
        await q.answer("Game already started!", show_alert=True)
        return True

    if user_id in game['players']:
        await q.answer("Already joined!", show_alert=True)
        return True

    if len(game['players']) >= 4:
        await q.answer("Lobby full!", show_alert=True)
        return True

    # SAFEGUARD: Check if free_spaces is empty
    if not game['free_spaces']:
        await q.answer("No available spaces!", show_alert=True)
        snake_manager.end_game(chat_id)
        return True

    # Add player with random position
    start_pos = random.choice(game['free_spaces'])
    game['players'][user_id] = {
        'body': [start_pos],
        'direction': random.choice(['up', 'down', 'left', 'right']),
        'score': 0,
        'name': q.from_user.first_name
    }
    game['player_order'].append(user_id)
    snake_manager.update_free_spaces(chat_id)

    # Update lobby message
    player_count = len(game['players'])
    await client.edit_message_text(
        chat_id=chat_id,
        message_id=game['message_id'],
        text=f"🐍 **Snake Battle Arena**\n"
             f"Host: {client.get_chat(snake_manager.creators[chat_id]).first_name}\n"
             f"Players: {player_count}/4\n"
             f"Status: {'Waiting...' if player_count <4 else 'Starting...'}\n"
             f"Use /over to cancel game",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
            "🎮 Join Battle", 
            callback_data=f"snake_join_{chat_id}"
        )]])
    )

    # Start game when 4 players join
    if player_count == 4:
        game['status'] = 'playing'
        game['start_time'] = time.time()
        current_player = snake_manager.get_current_player(chat_id)
        await update_board(
            client, game,
            f"🏁 Game Started!\n"
            f"First turn: {game['players'][current_player]['name']}"
        )

    await q.answer()
    return True

async def handle_move(q, game, user_id, direction, chat_id):
    if game['status'] != 'playing':
        await q.answer("Game not active!", show_alert=True)
        return True

    current_player = snake_manager.get_current_player(chat_id)
    if user_id != current_player:
        await q.answer(
            f"⏳ {game['players'][current_player]['name']}'s turn!",
            show_alert=True
        )
        return True

    snake = game['players'][user_id]
    # Prevent 180° turn
    if (snake['direction'], direction) in [('up','down'), ('down','up'), 
                                         ('left','right'), ('right','left')]:
        await q.answer("Can't reverse direction!", show_alert=True)
        return True

    # Update direction
    snake['direction'] = direction

    # Calculate new head position
    head_x, head_y = snake['body'][0]
    new_head = (
        head_x + (-1 if direction == 'up' else 1 if direction == 'down' else 0),
        head_y + (-1 if direction == 'left' else 1 if direction == 'right' else 0)
    )

    # Collision check
    collision = new_head in game['walls']
    if not collision:
        collision = any(new_head in p['body'] for pid, p in game['players'].items() if pid != user_id)

    if collision:
        snake_manager.remove_player(chat_id, user_id)
        await q.answer(f"💀 Collision! {q.from_user.first_name} eliminated!", show_alert=True)
    else:
        snake['body'].insert(0, new_head)
        if new_head == game['food']:
            snake['score'] += 10
            snake_manager.generate_food(chat_id)
        else:
            snake['body'].pop()
        snake_manager.update_free_spaces(chat_id)

    # Check game end
    if len(game['players']) == 1:
        winner_id = next(iter(game['players'].keys()))
        winner = await User.get(winner_id)
        winner.crystals += 15
        await winner.update()
        await add_snake_game(winner_id, list(game['players'].keys()), game['start_time'])
        await q.message.edit_text(
            f"🏆 Winner: {winner.user.first_name}\n"
            f"Score: {game['players'][winner_id]['score']} | +15 Crystals!",
            reply_markup=None
        )
        snake_manager.end_game(chat_id)
    else:
        next_player = snake_manager.next_turn(chat_id)
        await update_board(
            q.client, game,
            f"⏭️ Next turn: {game['players'][next_player]['name']}"
        )

    await q.answer()
    return True

async def handle_quit(client, q, game, chat_id):
    if q.from_user.id == snake_manager.creators.get(chat_id):
        snake_manager.end_game(chat_id)
        await q.message.edit_text("🐍 Game canceled by host!")
    else:
        snake_manager.remove_player(chat_id, q.from_user.id)
        await q.answer(f"🚪 You left the game!", show_alert=True)
        await update_board(client, game)
    return True

async def update_board(client, game, text=None):
    try:
        current_player = snake_manager.get_current_player(game['chat_id'])
        status_text = f"Current turn: {game['players'][current_player]['name']}" if current_player else "Game Over"

        if text:
            status_text = f"{text}\n{status_text}"

        await client.edit_message_text(
            chat_id=game['chat_id'],
            message_id=game['message_id'],
            text=status_text,
            reply_markup=InlineKeyboardMarkup(create_snake_board(game))
        )
    except Exception as e:
        print(f"Board update error: {e}")