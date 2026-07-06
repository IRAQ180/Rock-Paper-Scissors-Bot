from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

router = Router()

# 1. عند كتابة @اسم_البوت في أي محادثة (للبدء)
@router.inline_query()
async def inline_game(inline_query: InlineQuery):
    results = [
        InlineQueryResultArticle(
            id="start_vs",
            title="تحدَّ صديقك في حجرة ورقة مقص! ⚔️",
            description="اضغط لإرسال دعوة تحدي",
            input_message_content=InputTextMessageContent(
                message_text="🎮 **تحدي جديد!**\n\nاضغط على الزر أدناه لبدء المباراة مع صديقك:"
            ),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⚔️ اضغط هنا للعب", callback_data="play_game")]
            ])
        )
    ]
    await inline_query.answer(results, cache_time=1)

# 2. كيبورد اللعب الفعلي (يظهر بعد الضغط على زر التحدي)
def get_game_keys():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="مقص ✂️", callback_data="choice_scissors"),
            InlineKeyboardButton(text="ورق 📄", callback_data="choice_paper"),
            InlineKeyboardButton(text="حجره 🪨", callback_data="choice_rock")
        ]
    ])

# 3. معالجة الضغط على زر التحدي
@router.callback_query(F.data == "play_game")
async def start_game(callback: CallbackQuery):
    await callback.message.edit_text(
        "تم قبول التحدي! ⚔️\n\nاختر حركتك الآن (أنت وصديقك):",
        reply_markup=get_game_keys()
    )

# 4. معالجة اختيار الحركة
@router.callback_query(F.data.startswith("choice_"))
async def handle_choice(callback: CallbackQuery):
    choice = callback.data.split("_")[1]
    await callback.answer(f"تم تسجيل اختيارك: {choice} ✅", show_alert=True)
