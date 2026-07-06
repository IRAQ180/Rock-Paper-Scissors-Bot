import asyncio
import os
from aiogram import Bot, Dispatcher
from handlers import router

# هذا الجزء يقوم بجلب التوكن من الإعدادات (Variables) التي وضعتها في Railway
TOKEN = os.getenv('TOKEN')

async def main():
    # التحقق من وجود التوكن
    if not TOKEN:
        print("خطأ: لم يتم العثور على TOKEN في إعدادات Railway!")
        return

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    # ربط المميزات الموجودة في ملف handlers.py
    dp.include_router(router)
    
    print("البوت يعمل الآن...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
