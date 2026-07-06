from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import random

router = Router()

# دالة الأزرار
def get_game_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="مقص ✂️", callback_data="scissors"),
            InlineKeyboardButton(text="ورق 📄", callback_data="paper"),
            InlineKeyboardButton(text="حجره 🪨", callback_data="rock")
        ]
    ])

# 1. الاستعلام المضمن
@router.inline_query()
async def inline_game(inline_query: InlineQuery):
    results = [
        InlineQueryResultArticle(
            id="game_board",
            title="لعبة حجرة ورقة مقص ✂️",
            description="اضغط للعب مع صديقك",
            input_message_content=InputTextMessageContent(
                message_text="✂️ حجرة ورقة مقص\n👤 اضغط على الزر للعب مع صديقك:"
            ),
            reply_markup=get_game_buttons()
        )
    ]
    await inline_query.answer(results, cache_time=1, is_personal=False)

# 2. منطق النتيجة المنبثقة
@router.callback_query(F.data.in_(["rock", "paper", "scissors"]))
async def callback_handler(callback: CallbackQuery):
    player_choice = callback.data
    bot_choice = random.choice(["rock", "paper", "scissors"])
    
    # تحديد الفائز
    if player_choice == bot_choice:
        result = "تعادل! 🤝"
    elif (player_choice == "rock" and bot_choice == "scissors") or \
         (player_choice == "paper" and bot_choice == "rock") or \
         (player_choice == "scissors" and bot_choice == "paper"):
        result = "أنت الفائز! 🎉"
    else:
        result = "خسرت أمام البوت! 🤖"

    # هذا السطر يظهر النتيجة فوراً في نافذة منبثقة (Alert)
    await callback.answer(
        text=f"اختيارك: {player_choice}\nاختيار الخصم: {bot_choice}\n\n{result}",
        show_alert=True
    )
