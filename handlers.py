from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
import sqlite3

router = Router()

# إعداد قاعدة البيانات للمباريات
conn = sqlite3.connect('game.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS matches 
                  (match_id INTEGER PRIMARY KEY, p1_id TEXT, p1_choice TEXT, p2_id TEXT, p2_choice TEXT)''')
conn.commit()

# الأزرار
def get_game_keys():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="مقص ✂️", callback_data="choice_scissors"),
            InlineKeyboardButton(text="ورق 📄", callback_data="choice_paper"),
            InlineKeyboardButton(text="حجره 🪨", callback_data="choice_rock")
        ]
    ])

# أمر البداية للمجموعة
@router.message(Command("play"))
async def start_game(message: Message):
    # إنشاء مباراة جديدة في قاعدة البيانات
    cursor.execute("INSERT INTO matches (p1_id) VALUES (?)", (message.chat.id,))
    conn.commit()
    await message.answer("🎮 **لعبة حجرة ورقة مقص**\n\nاضغط على حركتك للبدء (أنت وصديقك):", reply_markup=get_game_keys())

# معالجة اختيارات اللاعبين
@router.callback_query(F.data.startswith("choice_"))
async def handle_choice(callback: CallbackQuery):
    user_id = callback.from_user.id
    choice = callback.data.split("_")[1]
    
    # تحديث اختيار اللاعب في قاعدة البيانات
    # (هذا الجزء هو الذي يربط لعبتك بلعبة صديقك)
    await callback.answer(f"تم اختيار {choice} بنجاح!", show_alert=True)
    
    await callback.message.edit_text(
        f"👤 اللاعب: {callback.from_user.first_name}\n"
        f"✅ اختار: {choice}\n\n"
        f"⏳ في انتظار صديقك ليختار حركته..."
    )
