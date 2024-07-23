@Client.on_message(filters.command("wtop"))
@YxH(private=False)
async def wtop(client, message):
    dic = await get_wordle_dic()
    if not dic:
        return await message.reply("Wordle leaderboard empty!")
    ok = await message.reply("Getting Wordle leaderboard...")
    nset = {y: int(dic[y]) for y in dic}
    dic = sorted(nset.items(), key=lambda x: x[1], reverse=True)
    txt = "Wordle Leaderboard\n\n"
    a = 1
    for i in dic:
        avg = await get_avg(int(i[0]))
        txt += f'{a}. {(await client.get_users(int(i[0]))).mention} :- {i[1]} ({str(avg)[:4] if len(str(avg)) > 4 else str(avg)})\n'
        a += 1
        if a > 10:
            break
    await ok.edit(txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data=f'close_{message.from_user.id}')]]))