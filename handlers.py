from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

router = Router()

# كيبورد اللعبة
def get_game_keys():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="مقص ✂️", callback_data="choice_scissors"),
            InlineKeyboardButton(text="ورق 📄", callback_data="choice_paper"),
            InlineKeyboardButton(text="حجره 🪨", callback_data="choice_rock")
        ]
    ])

# 1. ابدأ التحدي بكتابة /play في المجموعة
@router.message(Command("play"))
async def start_game(message: Message):
    # هذه الرسالة يرسلها البوت، لذا يملك صلاحية تعديلها بالكامل!
    await message.answer(
        "🎮 **مباراة حجرة ورقة مقص**\n\nاضغط على حركتك للتحدي:",
        reply_markup=get_game_keys()
    )

# 2. معالجة الضغط (سيعمل التعديل الآن فوراً وبدون أي أخطاء)
@router.callback_query(F.data.startswith("choice_"))
async def handle_choice(callback: CallbackQuery):
    choice = callback.data.split("_")[1]
    user_name = callback.from_user.first_name
    
    # بما أن الرسالة أصلية، هذا السطر سيعمل 100%
    await callback.message.edit_text(
        f"✅ تم تسجيل اختيار {user_name}: {choice}\n\n"
        f"⏳ في انتظار صديقك ليختار حركته..."
    )
    await callback.answer("تم تسجيل اختيارك!")
