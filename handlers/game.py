from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import random

router = Router()

@router.message(Command("game"))
async def start_game(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪨", callback_data="rock"), 
         InlineKeyboardButton(text="📄", callback_data="paper"),
         InlineKeyboardButton(text="✂️", callback_data="scissors")]
    ])
    await message.answer("اختر حركتك:", reply_markup=keyboard)

@router.callback_query(F.data.in_(["rock", "paper", "scissors"]))
async def play(callback: CallbackQuery):
    user_move = callback.data
    bot_move = random.choice(["rock", "paper", "scissors"])
    
    if user_move == bot_move:
        await callback.message.edit_text("تعادل! 🤝")
    elif (user_move == "rock" and bot_move == "scissors") or \
         (user_move == "paper" and bot_move == "rock") or \
         (user_move == "scissors" and bot_move == "paper"):
        await callback.message.edit_text("فزت! 🎉")
    else:
        await callback.message.edit_text("خسرت! 🤖")

