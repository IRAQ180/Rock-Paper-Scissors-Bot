from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

router = Router()

# هذا الزر هو السر: يفتح قائمة البوت فوراً عند الضغط عليه
def get_start_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚔️ اضغط للبدء في التحدي", switch_inline_query_current_chat="")]
    ])

# 1. عند كتابة @اسم_البوت
@router.inline_query()
async def inline_game(inline_query: InlineQuery):
    # إذا لم يكتب المستخدم شيئاً، نظهر له أزرار اللعبة
    if not inline_query.query:
        results = [
            InlineQueryResultArticle(
                id="game_buttons",
                title="لعبة حجرة ورقة مقص ✂️",
                description="اضغط هنا لبدء التحدي",
                input_message_content=InputTextMessageContent(message_text="🎮 **مباراة جديدة!**\nاختر حركتك:"),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="مقص ✂️", callback_data="scissors"),
                        InlineKeyboardButton(text="ورق 📄", callback_data="paper"),
                        InlineKeyboardButton(text="حجره 🪨", callback_data="rock")
                    ]
                ])
            )
        ]
        await inline_query.answer(results, cache_time=1)

# 2. معالجة الضغط (بشكل يمنع التحميل)
@router.callback_query(F.data.in_(["rock", "paper", "scissors"]))
async def handle_choice(callback: CallbackQuery):
    choice = callback.data
    # رد فوري ينهي حالة التحميل ويظهر النتيجة
    await callback.answer(f"✅ تم تسجيل اختيارك: {choice}\nفي انتظار صديقك...", show_alert=True)
