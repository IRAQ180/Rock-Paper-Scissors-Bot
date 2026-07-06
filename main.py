import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# ضع التوكن الخاص بك هنا بين علامات تنصيص مستقيمة
TOKEN = '8201679973:AAFa6xGpxL7PxXX3s1QbNEXkMjy5Ah6kvcM'

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('مرحباً! اختر: حجرة، ورقة، أو مقص.')

@dp.message(F.text.in_(['حجرة', 'ورقة', 'مقص']))
async def game_handler(message: types.Message):
    user_choice = message.text
    # هنا تضع منطق اللعبة الخاص بك
    await message.answer(f'لقد اخترت: {user_choice}')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
