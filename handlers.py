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

# 1. عند كتابة @اسم_البوت - يرسل الزر فقط
@router.inline_query()
async def inline_game(inline_query: InlineQuery):
    results = [
        InlineQueryResultArticle(
            id="start_match",
            title="⚔️ تحدي حجرة ورقة مقص",
            description="اضغط للبدء",
            input_message_content=InputTextMessageContent(message_text="🎮 **مباراة جديدة!**\nاضغط على الزر أدناه لبدء التحدي:"),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⚔️ اضغط للبدء", callback_data="join_game")]
            ])
        )
    ]
    await inline_query.answer(results, cache_time=1)

# 2. اللحظة الحاسمة: تحويل التحدي لرسالة بوت فعلية تعمل باللمس
@router.callback_query(F.data == "join_game")
async def join_game(callback: CallbackQuery):
    # هنا نقوم بإنشاء رسالة جديدة تماماً من البوت نفسه، 
    # هذه الرسالة ستكون قابلة للتعديل 100% ولن تعلق أبداً
    await callback.message.answer(
        "⚔️ تم فتح المباراة! \nاختر حركتك:",
        reply_markup=get_game_keys()
    )
    await callback.answer()

# 3. معالجة الحركة
@router.callback_query(F.data.startswith("choice_"))
async def handle_choice(callback: CallbackQuery):
    choice = callback.data.split("_")[1]
    # بما أن الرسالة أصبحت "رسالة بوت"، التعديل سيعمل فوراً بدون مشاكل
    await callback.message.edit_text(f"👤 تم اختيار: {choice}\n⏳ في انتظار الخصم...")
