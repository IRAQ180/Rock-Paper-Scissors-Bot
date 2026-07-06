from aiogram import Router, F
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router()

# هذا الكود يجعل البوت يرسل "نتيجة" فقط، بدون رسائل نصية معقدة
@router.inline_query()
async def inline_game(inline_query: InlineQuery):
    # زر شفاف يفتح قائمة البوت عند الضغط عليه
    results = [
        InlineQueryResultArticle(
            id="transparent_game",
            title="⚔️ تحدي حجرة ورقة مقص",
            input_message_content=InputTextMessageContent(message_text="🎮 **تحدي جديد!** اضغط للبدء:"),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="مقص ✂️", callback_data="choice_s"),
                    InlineKeyboardButton(text="ورق 📄", callback_data="choice_p"),
                    InlineKeyboardButton(text="حجره 🪨", callback_data="choice_r")
                ]
            ])
        )
    ]
    await inline_query.answer(results, cache_time=1, is_personal=False)

# هذا الجزء هو المسؤول عن "الشفافية"
@router.callback_query(F.data.startswith("choice_"))
async def handle_choice(callback: CallbackQuery):
    # بدلاً من تعديل الرسالة (الذي يسبب الدوران)، نستخدم تنبيهاً فقط
    await callback.answer(
        text=f"✅ تم تسجيل حركتك: {callback.data.split('_')[1]}\nانتظر نتيجة صديقك!",
        show_alert=True
    )
