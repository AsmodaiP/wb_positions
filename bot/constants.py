"""Constants for the bot."""

import os

from dotenv import load_dotenv
from telegram import KeyboardButton, ReplyKeyboardMarkup

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

BOT_MAIN_MENU = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Поиск"),
            KeyboardButton("Популярные запросы"),
        ],
        [
            KeyboardButton("Поиск по популярным запросам"),
        ]


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
