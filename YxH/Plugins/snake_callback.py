from pyrogram.types import CallbackQuery
import random
from ..Utils.snake import snake_manager, create_snake_board
from ..Database.snake import add_snake_game
from ..Class.user import User

async def handle_snake_game(client, q: CallbackQuery):
    if not q.data.startswith("snake_"):
        return False  # Not our callback
    
    try:
        parts = q.data.split('_')
        action = parts[1]
        chat_id = int(parts[2])
        game = snake_manager.get_game(chat_id)
        user_id = q.from_user.id
        
        await q.answer()

        if not game:
            await q.edit_message_text("🐍 Game session expired!")
            return True

        if action == "dir":
            direction = parts[3]
            await _handle_snake_move(q, game, user_id, direction)
        elif action == "join":
            if len(game['players']) < 4:
                start_pos = random.choice(game['free_spaces'])
                game['players'][user_id] = {
                    'body': [start_pos],
                    'direction': random.choice(['up', 'down', 'left', 'right']),
                    'score': 0
                }
                snake_manager.update_free_spaces(chat_id)
                await _update_snake_board(q, game, 
                    f"👤 {q.from_user.first_name} joined!\nPlayers: {len(game['players'])}/4")
        elif action == "quit":
            snake_manager.end_game(chat_id)
            await q.edit_message_text("🐍 Game canceled!")

        return True  # Handled successfully

    except Exception as e:
        print(f"Snake error: {e}")
        await q.answer("🐍 Game reset!", show_alert=True)
        snake_manager.end_game(chat_id)
        return True

async def _handle_snake_move(q: CallbackQuery, game, user_id, direction):
    if user_id not in game['players']:
        return await q.answer("Join the game first!", show_alert=True)
    
    snake = game['players'][user_id]
    current_dir = snake['direction']
    
    if (current_dir, direction) in [('up', 'down'), ('down', 'up'), 
                                   ('left', 'right'), ('right', 'left')]:
        return await q.answer("Can't reverse direction!", show_alert=True)
    
    snake['direction'] = direction
    head = snake['body'][0]
    new_head = (
        head[0] + (-1 if direction == 'up' else 1 if direction == 'down' else 0),
        head[1] + (-1 if direction == 'left' else 1 if direction == 'right' else 0)
    )
    
    # Collision check
    collision = new_head in game['walls']
    if not collision:
        for pid, p in game['players'].items():
            if pid != user_id and new_head in p['body']:
                collision = True
                break
    
    if collision:
        snake_manager.remove_player(game['chat_id'], user_id)
        await q.answer(f"💀 {q.from_user.first_name} crashed!", show_alert=True)
    else:
        snake['body'].insert(0, new_head)
        if new_head == game['food']:
            snake['score'] += 10
            game['food'] = snake_manager.generate_food(game['chat_id'])
        else:
            snake['body'].pop()
        snake_manager.update_free_spaces(game['chat_id'])
    
    if len(game['players']) <= 1:
        winner_id = next(iter(game['players'].keys()), None)
        if winner_id:
            winner = await User.get(winner_id)
            winner.crystals += 2
            await winner.update()
            await add_snake_game(winner_id, list(game['players'].keys()), game['start_time'])
            await q.edit_message_text(
                f"🏆 {q.from_user.first_name} wins!\n+15 crystals earned! 💎",
                reply_markup=None
            )
        snake_manager.end_game(game['chat_id'])
    else:
        await _update_snake_board(q, game)

async def _update_snake_board(q: CallbackQuery, game, text=None):
    markup = create_snake_board(game)
    try:
        if text:
            await q.edit_message_text(
                f"{text}\n🕹️ Current Players: {len(game['players'])}\n"
                f"⏳ Running for: {int(time.time() - game['start_time'])}s",
                reply_markup=InlineKeyboardMarkup(markup)
            )
        else:
            await q.edit_message_reply_markup(InlineKeyboardMarkup(markup))
    except Exception as e:
        print(f"Error updating board: {e}")