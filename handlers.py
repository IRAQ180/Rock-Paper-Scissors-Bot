from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

router = Router()

# دالة الأزرار
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
            id="vs_friend",
            title="تحدَّ صديقك! ⚔️",
            input_message_content=InputTextMessageContent(
                message_text="🎮 **مباراة حجرة ورقة مقص**\nاضغط على حركتك للتحدي:"
            ),
            reply_markup=get_game_keys()
        )
    ]
    await inline_query.answer(results, cache_time=1)

# 2. الاستجابة الفورية (لا تستخدم edit_text نهائياً)
@router.callback_query(F.data.startswith("choice_"))
async def handle_choice(callback: CallbackQuery):
    choice = callback.data.split("_")[1]
    user_name = callback.from_user.first_name
    
    # الرد المنبثق (Alert) يعمل دائماً لأن تليجرام لا يمنعه
    await callback.answer(
        text=f"👤 {user_name}\n✅ اختار: {choice}\n\nالآن دور صديقك ليضغط على حركته!",
        show_alert=True
    )
