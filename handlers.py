from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router()

# إنشاء لوحة الأزرار (Inline Keyboard)
def get_game_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🪨 حجرة", callback_data="rock"),
            InlineKeyboardButton(text="📄 ورقة", callback_data="paper"),
            InlineKeyboardButton(text="✂️ مقص", callback_data="scissors")
        ]
    ])
    return keyboard

# أمر البدء لإظهار الأزرار
@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("أهلاً بك! اختر لعبتك المفضلة من الأزرار أدناه:", reply_markup=get_game_keyboard())

# التعامل مع ضغطات الأزرار (Callbacks)
@router.callback_query(F.data.in_(["rock", "paper", "scissors"]))
async def game_callback(callback: CallbackQuery):
    choice = callback.data
    await callback.answer(f"لقد اخترت: {choice}") # رسالة مؤقتة فوق الزر
    await callback.message.edit_text(f"لقد اخترت: {choice}! هل تود اللعب مرة أخرى؟", reply_markup=get_game_keyboard())
