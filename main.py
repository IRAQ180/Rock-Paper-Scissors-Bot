import asyncio
from aiogram import Bot, Dispatcher
from handlers.game import router

# ضع التوكن الخاص بك هنا
TOKEN = "8201679973:AAFa6xGpxL7PxXX3s1QbNEXkMjy5Ah6kvcM"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    print("البوت يعمل الآن...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
؛ 
