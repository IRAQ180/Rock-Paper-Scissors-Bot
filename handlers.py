from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import sqlite3

router = Router()

# إعداد قاعدة البيانات لحفظ حالة اللعبة
conn = sqlite3.connect('game.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, player1 TEXT, choice1 TEXT, player2 TEXT, choice2 TEXT)')
conn.commit()

# أزرار اللعبة
def get_game_keys():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="مقص ✂️", callback_data="choice_scissors"),
            InlineKeyboardButton(text="ورق 📄", callback_data="choice_paper"),
            InlineKeyboardButton(text="حجره 🪨", callback_data="choice_rock")
        ]
    ])

# 1. الاستعلام المضمن
@router.inline_query()
async def inline_game(inline_query: InlineQuery):
    results = [
        InlineQueryResultArticle(
            id="start_match",
            title="لعبة حجرة ورقة مقص ✂️",
            input_message_content=InputTextMessageContent(
                message_text="🎮 تحدي جديد! اضغط على حركتك للبدء:"
            ),
            reply_markup=get_game_keys()
        )
    ]
    await inline_query.answer(results, cache_time=1)

# 2. منطق تسجيل الحركة
@router.callback_query(F.data.startswith("choice_"))
async def handle_choice(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_name = callback.from_user.first_name
    choice = callback.data.split("_")[1]
    
    # تسجيل الاختيار في قاعدة البيانات (تبسيط للمنطق)
    await callback.answer(f"تم تسجيل اختيارك: {choice} ✅\nفي انتظار صديقك...", show_alert=True)
