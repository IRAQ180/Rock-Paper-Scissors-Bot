from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import random

router = Router()

def get_game_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="مقص ✂️", callback_data="scissors"),
            InlineKeyboardButton(text="ورق 📄", callback_data="paper"),
            InlineKeyboardButton(text="حجره 🪨", callback_data="rock")
        ]
    ])

@router.inline_query()
async def inline_game(inline_query: InlineQuery):
    results = [
        InlineQueryResultArticle(
            id="game_board",
            title="لعبة حجرة ورقة مقص",
            input_message_content=InputTextMessageContent(
                message_text="حجرة ورقة مقص ✂️\nاضغط للعب مع ( ) 👤"
            ),
            reply_markup=get_game_buttons()
        )
    ]
    await inline_query.answer(results, cache_time=1)

@router.callback_query(F.data.in_(["rock", "paper", "scissors"]))
async def callback_handler(callback: CallbackQuery):
    # إرسال رد فوري لتليجرام لإنهاء حالة التحميل
    await callback.answer()
    
    player_choice = callback.data
    bot_choice = random.choice(["rock", "paper", "scissors"])
    
    # تحديد النتيجة
    if player_choice == bot_choice:
        result = "تعادل! 🤝"
    elif (player_choice == "rock" and bot_choice == "scissors") or \
         (player_choice == "paper" and bot_choice == "rock") or \
         (player_choice == "scissors" and bot_choice == "paper"):
        result = "أنت الفائز! 🎉"
    else:
        result = "لقد فزتُ أنا! 🤖"

    # استخدام try/except لتجنب توقف البوت في حال فشل التعديل
    try:
        await callback.message.edit_text(
            f"اختيارك: {player_choice}\n"
            f"اختيار البوت: {bot_choice}\n\n"
            f"النتيجة: {result}"
        )
    except Exception as e:
        print(f"خطأ في التعديل: {e}")
