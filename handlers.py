from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import random

router = Router()

# قاموس لتخزين نتائج اللاعبين (ID اللاعب: [فوز، خسارة])
user_scores = {}

def get_game_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🪨 حجرة", callback_data="rock"),
            InlineKeyboardButton(text="📄 ورقة", callback_data="paper"),
            InlineKeyboardButton(text="✂️ مقص", callback_data="scissors")
        ],
        [InlineKeyboardButton(text="❌ إنهاء اللعبة", callback_data="quit")]
    ])
    return keyboard

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    user_scores[message.from_user.id] = [0, 0] # تصفير النتيجة
    await message.answer("أهلاً بك في لعبة التحدي! اختر رمزاً:", reply_markup=get_game_keyboard())

@router.callback_query(F.data.in_(["rock", "paper", "scissors"]))
async def game_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_scores:
        user_scores[user_id] = [0, 0]

    player_choice = callback.data
    bot_choice = random.choice(["rock", "paper", "scissors"])
    
    result = ""
    if player_choice == bot_choice:
        result = "تعادل! 🤝"
    elif (player_choice == "rock" and bot_choice == "scissors") or \
         (player_choice == "paper" and bot_choice == "rock") or \
         (player_choice == "scissors" and bot_choice == "paper"):
        result = "أحسنت، لقد فزت! 🎉"
        user_scores[user_id][0] += 1
    else:
        result = "للأسف، لقد فزتُ أنا! 🤖"
        user_scores[user_id][1] += 1

    text = (f"خيارك: {player_choice}\nخيار البوت: {bot_choice}\n\n"
            f"النتيجة: {result}\n\n"
            f"النقاط: {user_scores[user_id][0]} فوز - {user_scores[user_id][1]} خسارة")
    
    await callback.message.edit_text(text, reply_markup=get_game_keyboard())

@router.callback_query(F.data == "quit")
async def quit_game(callback: CallbackQuery):
    await callback.message.edit_text("شكراً للعب! إذا أردت اللعب مجدداً أرسل /start")
