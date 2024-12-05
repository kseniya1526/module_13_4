from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


api = "7689512789:AAHgPkfxoHEfc2Yr2MCe8g-6FnRJsYLeADY"

bot = Bot(token=api)

dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text= 'Calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age= message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth= message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight= message.text)
    data = await state.get_data()
    norma_calories = 10 * float(data["weight"]) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
    await message.answer(f"Ваша норма калорий: {norma_calories} ккал в день.")
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.")
    await message.answer('Если хотите узнать свою норму калорий, введите команду: Calories.')


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)