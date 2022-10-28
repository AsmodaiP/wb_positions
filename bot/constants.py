from dotenv import load_dotenv
import os
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

BOT_MAIN_MENU = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Поиск"),
            KeyboardButton("Избранное"),
        ],
    ],
    resize_keyboard=True,
)

SKIP_MENU = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Пропустить"),
        ],
    ],
    resize_keyboard=True,
)
