from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import sqlite3

router = Router()

# إنشاء قاعدة بيانات لحفظ المباراة
conn = sqlite3.connect('game.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS matches 
                  (match_id TEXT PRIMARY KEY, player1_choice TEXT, player2_choice TEXT)''')
conn.commit()

def get_game_keys():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="مقص ✂️", callback_data="choice_scissors"),
            InlineKeyboardButton(text="ورق 📄", callback_data="choice_paper"),
            InlineKeyboardButton(text="حجره 🪨", callback_data="choice_rock")
        ]
    ])

@router.inline_query()
async def inline_game(inline_query: InlineQuery):
    # إنشاء معرف للمباراة (مثلاً استخدام اسم المستخدم كمفتاح)
    match_id = str(inline_query.from_user.id)
    
    results = [
        InlineQueryResultArticle(
            id="start_match",
            title="⚔️ تحدي حجرة ورقة مقص",
            input_message_content=InputTextMessageContent(message_text="🎮 اختر حركتك لبدء التحدي:"),
            reply_markup=get_game_keys()
        )
    ]
    await inline_query.answer(results, cache_time=1)

@router.callback_query(F.data.startswith("choice_"))
async def handle_choice(callback: CallbackQuery):
    choice = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    # التحقق من وجود مباراة
    cursor.execute("SELECT * FROM matches WHERE match_id = ?", (str(user_id),))
    match = cursor.fetchone()
    
    if not match:
        # إذا لم توجد مباراة، يتم بدء واحدة جديدة
        cursor.execute("INSERT INTO matches (match_id, player1_choice) VALUES (?, ?)", (str(user_id), choice))
        conn.commit()
        await callback.answer("تم تسجيل اختيارك! أرسل رابط اللعبة لصديقك ليدخل التحدي.", show_alert=True)
    else:
        # إذا كانت موجودة، يتم تسجيل اختيار الطرف الثاني وإعلان النتيجة
        cursor.execute("UPDATE matches SET player2_choice = ? WHERE match_id = ?", (choice, str(user_id)))
        conn.commit()
        await callback.answer(f"تمت المقارنة! النتيجة ستظهر في المجموعة.", show_alert=True)
