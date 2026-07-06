from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import random

router = Router()

# دالة الأزرار للعب المباشر
def get_game_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🪨 حجرة", callback_data="rock"),
            InlineKeyboardButton(text="📄 ورقة", callback_data="paper"),
            InlineKeyboardButton(text="✂️ مقص", callback_data="scissors")
        ]
    ])

# 1. الاستعلام المضمن (تظهر عند كتابة @اسم_البوت)
@router.inline_query()
async def inline_game(inline_query: InlineQuery):
    results = [
        InlineQueryResultArticle(
            id="game",
            title="لعبة حجرة ورقة مقص 🎮",
            description="اضغط للعب مع صديقك",
            input_message_content=InputTextMessageContent(message_text="لعبة جديدة! اختر حركتك الآن:"),
            reply_markup=get_game_buttons()
        )
    ]
    await inline_query.answer(results, cache_time=1)

# 2. التعامل مع ضغطات الأزرار
@router.callback_query(F.data.in_(["rock", "paper", "scissors"]))
async def handle_buttons(callback: CallbackQuery):
    player_choice = callback.data
    options = ["rock", "paper", "scissors"]
    # اختيار عشوائي للخصم (البوت)
    bot_choice = random.choice(options)
    
    # تحديد النتيجة
    if player_choice == bot_choice:
        result = "تعادل! 🤝"
    elif (player_choice == "rock" and bot_choice == "scissors") or \
         (player_choice == "paper" and bot_choice == "rock") or \
         (player_choice == "scissors" and bot_choice == "paper"):
        result = "أنت الفائز! 🎉"
    else:
        result = "للأسف، خسرت هذه الجولة! 🤖"

    # تحديث الرسالة بالنتيجة
    text = (f"النتيجة:\n"
            f"اختيارك: {player_choice}\n"
            f"اختيار الخصم: {bot_choice}\n\n"
            f"{result}")
    
    await callback.message.edit_text(text)
