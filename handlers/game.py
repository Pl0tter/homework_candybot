from loader import dp
from aiogram import types
import game_db
import random


@dp.message_handler()
async def mes_take(message: types.Message):
    for duel in game_db.total:
        if message.from_user.id == duel[0] and len(duel) == 4:
            count = message.text
            if count.isdigit() and 0 < int(count) < 29:
                duel[2] -= int(count)
                if await check_win(message, 'Ты', duel):
                    return True
                await message.answer(f'{duel[1]} взял {count} конфет и на столе осталось {duel[2]}\n'
                                     f'Теперь ход бота')
                if duel[3] == 'easy':
                    bot_take = random.randint(
                        1, 28) if duel[2] > 28 else duel[2]
                elif duel[3] == 'hard':
                    bot_take = random.randint(
                        1, 28) if duel[2] % 29 == 0 else duel[2] % 29
                duel[2] -= bot_take
                if await check_win(message, 'Бот', duel):
                    return True
                await message.answer(f'Бот взял {bot_take} конфет и на столе осталось {duel[2]}\n'
                                     f'Теперь твой ход')
            else:
                await message.answer(f'Введите число от 1 до 28')


async def check_win(message: types.Message, win: str, duel: list):
    if duel[2] <= 0:
        await message.answer(f'{win} победил! Поздравляю! Чтобы начать заново, отправь /start')
        game_db.total.remove(duel)
        return True
    return False
