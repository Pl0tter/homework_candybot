from loader import dp
from aiogram import types


@dp.message_handler(commands=['help'])
async def mes_help(message: types.Message):
    await message.answer(f'Чем могу помочь?')
