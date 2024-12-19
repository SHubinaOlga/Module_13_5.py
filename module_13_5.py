from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard = True)
button = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text = 'Информация')
kb.row(button, button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start_massage(massage):
    await massage.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text='Рассчитать')
async def set_age(massage):
    await massage.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(text = 'Информация')
async def inform_massages(message):
    await message.answer('Бот, рассчитывающий норму ккал по упрощенной формуле Миффлина-Сан Жеора.')

@dp.message_handler(state=UserState.age)
async def set_growth(massage, state):
    await state.update_data(age=massage.text)
    await massage.answer(f' Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(massage, state):
    await state.update_data(growth=massage.text)
    await massage.answer(f' Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(massage, state):
    await state.update_data(weight=massage.text)
    data = await state.get_data()

    men = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    women = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161

    await massage.answer(f' Ваша норма калорий в сутки: 1) Для женщин: {women} ккал, 2) Для мужчин: {men}')
    await UserState.weight.set()
    await state.finish()

@dp.message_handler()
async def all_massages(massage):
    await massage.answer('Введите команду start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)