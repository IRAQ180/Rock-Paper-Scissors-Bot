from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import random

router = Router()

# 1. كيبورد اللعب الفردي
def get_game_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🪨 حجرة", callback_data="rock"),
            InlineKeyboardButton(text="📄 ورقة", callback_data="paper"),
            InlineKeyboardButton(text="✂️ مقص", callback_data="scissors")
        ]
    ])

# 2. بداية اللعب الفردي
@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("أهلاً بك! اختر رمزاً للبدء:", reply_markup=get_game_keyboard())

@router.callback_query(F.data.in_(["rock", "paper", "scissors"]))
async def game_callback(callback: CallbackQuery):
    player_choice = callback.data
    bot_choice = random.choice(["rock", "paper", "scissors"])
    
    result = "تعادل 🤝"
    if (player_choice == "rock" and bot_choice == "scissors") or \
       (player_choice == "paper" and bot_choice == "rock") or \
       (player_choice == "scissors" and bot_choice == "paper"):
        result = "أنت الفائز! 🎉"
    elif player_choice != bot_choice:
        result = "البوت هو الفائز! 🤖"

    await callback.message.edit_text(f"أنت: {player_choice}\nالبوت: {bot_choice}\n\nالنتيجة: {result}")

# 3. ميزة تحدي الأصدقاء عبر الاستعلام المضمن
@router.inline_query()
async def inline_game(inline_query: InlineQuery):
    # زر التحدي الذي سيظهر مع كل خيار
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="تحدَّني!", switch_inline_query="")]
    ])
    
    results = [
        InlineQueryResultArticle(
            id="rock", title="حجرة 🪨",
            input_message_content=InputTextMessageContent(message_text="لقد اخترت: حجرة 🪨. دورك الآن يا صديقي!"),
            reply_markup=keyboard
        ),
        InlineQueryResultArticle(
            id="paper", title="ورقة 📄",
            input_message_content=InputTextMessageContent(message_text="لقد اخترت: ورقة 📄. دورك الآن يا صديقي!"),
            reply_markup=keyboard
        ),
        InlineQueryResultArticle(
            id="scissors", title="مقص ✂️",
            input_message_content=InputTextMessageContent(message_text="لقد اخترت: مقص ✂️. دورك الآن يا صديقي!"),
            reply_markup=keyboard
        )
    ]
    await inline_query.answer(results, cache_time=1)
