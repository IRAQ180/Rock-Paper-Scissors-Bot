from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

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

# 1. عند كتابة @اسم_البوت
@router.inline_query()
async def inline_game(inline_query: InlineQuery):
    results = [
        InlineQueryResultArticle(
            id="vs_friend",
            title="تحدَّ صديقك الآن! ⚔️",
            input_message_content=InputTextMessageContent(
                message_text="🎮 **مباراة حجرة ورقة مقص**\n\nاضغط على حركتك للبدء:"
            ),
            reply_markup=get_game_keys()
        )
    ]
    await inline_query.answer(results, cache_time=1)

# 2. معالجة اختيارات اللاعبين
# ملاحظة: هذا الكود يسجل الضغط ويظهر للطرفين ماذا اختاروا
@router.callback_query(F.data.startswith("choice_"))
async def handle_choice(callback: CallbackQuery):
    user_name = callback.from_user.first_name
    choice = callback.data.split("_")[1]
    
    # الرد يظهر للطرفين فوراً
    await callback.answer(
        f"{user_name} اختار: {choice}!\n\nانتظر صديقك ليختار حركته!", 
        show_alert=True
    )
