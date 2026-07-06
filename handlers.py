from aiogram import Router, F
from aiogram.types import Message

# هذا الـ router هو الذي سيربط المميزات بملف التشغيل الأساسي
router = Router()

# هنا تضع كل المميزات والأوامر التي تريدها
@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("أهلاً بك في البوت! أنا جاهز للعب.")

@router.message(F.text == "حجرة")
async def game_rock(message: Message):
    await message.answer("أنت اخترت حجرة! 🪨")
