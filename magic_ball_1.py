import asyncio
import os
import random
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import re

# ================== ЗАГРУЗКА .ENV ==================
dotenv_path = os.path.join(os.path.dirname(__file__), "1.env")
load_dotenv(dotenv_path=dotenv_path)

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError(f"Не найден токен! Проверьте файл .env в {dotenv_path}")

# ================== НАСТРОЙКИ ==================
ANSWERS = [
    "- Сбудется! ˚ ✩°｡⋆♡ ",
    "- Нет!   ⃠",
    "- Может быть𓏧",
    "- Определённое «да»",
    "- Сомнительно 𓁺",
    "- Попробуй снова  ⃕"
]

# ================== КНОПКИ ==================
# Кнопка для приветствия
keyboard_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⊹ Кручусь волчком ⊹‫",
                callback_data="choice"
            )
        ]
    ]
)

# Кнопки для следующего вопроса
keyboard_next = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="𓂃𓂃𓂃Ещё раз?𓂃𓂃𓂃",
                callback_data="choice"
            )
        ],
        [
            InlineKeyboardButton(
                text="〻 Перезапустить 〻\n",
                callback_data="restart"
            )
        ]
    ]
)

# ================== ФУНКЦИЯ ЭКРАНИРОВАНИЯ MARKDOWN ==================
def escape_markdown(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!\\"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

# ================== ROUTER ==================
router = Router()

@router.message(CommandStart())
async def start(message: Message):
    text = (
        "🔮 Привет!\n\nЯ — *Шар судьбы*, и я помогу тебе\nопределиться с выбором.\n\n"
        "Удобно расположись, сделай глубокий вдох.\nДоверься Проведению...\n\nМысленно задай вопрос.\n\nЖми на кнопку под\nэтим сообщением ↓"
    )
    await message.answer(
        text,
        reply_markup=keyboard_start,
        parse_mode=ParseMode.MARKDOWN
    )

@router.callback_query(lambda c: c.data == "choice")
async def choice(callback: CallbackQuery):
    answer = random.choice(ANSWERS)

    # Отправляем ответ Шара судьбы (без кнопок)
    await callback.message.answer(

        f"*Шар судьбы* говорит:\n\n{answer}\n\n​",
        parse_mode=ParseMode.MARKDOWN
    )
  # Следующее сообщение с инструкцией и кнопками
    await callback.message.answer(
        "[ ‧ s i t e ‧ m g b ‧ ](http://magball.ru)",
        reply_markup=keyboard_next,
        parse_mode=ParseMode.MARKDOWN_V2
    )

    await callback.answer()

@router.callback_query(lambda c: c.data == "restart")
async def restart_bot(callback: CallbackQuery):
    # Перезапуск бота: выводим приветствие с одной кнопкой
    await start(callback.message)
    await callback.answer()

# ================== ЗАПУСК ==================
async def main():
    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
