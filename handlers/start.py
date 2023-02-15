from loader import dp
from aiogram import types
import game_db


@dp.message_handler(commands=['start'])
async def mes_start(message: types.Message):
    if await check_start(message):
        await message.answer(f'Привет, {message.from_user.first_name}! '
                             f'Мы будем играть в конфеты. Сколько у нас конфет? Отправь set и количество конфет')


@dp.message_handler(lambda message: message.text and 'set' in message.text.lower())
async def mes_set(message: types.Message):
    if await check_start(message):
        if len(message.text.split()) > 1:
            if message.text.split()[1].isdigit():
                candies = int(message.text.split()[1])
                my_game = [message.from_user.id,
                           message.from_user.first_name, candies]
                game_db.total.append(my_game)
                await message.answer('Укажи сложность бота: /easy или /hard')
        else:
            await message.answer('Ты не ввел число после set')


@dp.message_handler(commands=['easy', 'hard'])
async def mes_level(message: types.Message):
    level = 'easy' if 'easy' in message.text and 'hard' not in message.text else 'hard'
    for duel in game_db.total:
        if message.from_user.id == duel[0]:
            duel.append(level)
            await message.answer('Начинаем! Бери от 1 до 28 конфет')


async def check_start(message: types.Message):
    for duel in game_db.total:
        if message.from_user.id == duel[0]:
            if len(duel) == 4:
                await message.answer('Ты уже начал игру! Бери от 1 до 28 конфет')
            return False
    else:
        return True
