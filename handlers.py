from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

router = Router()

# دالة الأزرار للعبة
def get_game_keys():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="مقص ✂️", callback_data="choice_scissors"),
            InlineKeyboardButton(text="ورق 📄", callback_data="choice_paper"),
            InlineKeyboardButton(text="حجره 🪨", callback_data="choice_rock")
        ]
    ])

# 1. الاستعلام المضمن: يرسل فقط زر "للدخول في التحدي"
@router.inline_query()
async def inline_game(inline_query: InlineQuery):
    results = [
        InlineQueryResultArticle(
            id="start_match",
            title="⚔️ تحدي حجرة ورقة مقص",
            description="اضغط هنا لفتح اللعبة في الرسائل الخاصة",
            input_message_content=InputTextMessageContent(
                message_text="🎮 **تم إنشاء مباراة!**\nاضغط على الزر أدناه لبدء اللعب مع صديقك:"
            ),
            # switch_inline_query_current_chat يفتح البوت مباشرة في المحادثة
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⚔️ اضغط للبدء", callback_data="start_game")]
            ])
        )
    ]
    await inline_query.answer(results, cache_time=1)

# 2. الاستجابة للضغط: هنا نرسل رسالة جديدة كلياً
@router.callback_query(F.data == "start_game")
async def start_game(callback: CallbackQuery):
    # إجابة فورية لمنع الدوران
    await callback.answer()
    
    # رسالة جديدة قابلة للتعديل 100%
    await callback.message.answer(
        "⚔️ المباراة بدأت! اختر حركتك:",
        reply_markup=get_game_keys()
    )

# 3. معالجة الحركة: التعديل هنا سيعمل فوراً بدون مشاكل
@router.callback_query(F.data.startswith("choice_"))
async def handle_choice(callback: CallbackQuery):
    choice = callback.data.split("_")[1]
    await callback.message.edit_text(
        f"✅ تم تسجيل اختيارك: {choice}\n⏳ في انتظار صديقك..."
    )
