"""Constants for the bot."""

import os
from typing import TypedDict

from dotenv import load_dotenv
from telegram import KeyboardButton, ReplyKeyboardMarkup

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


class KeyboardDict(TypedDict):
    search: KeyboardButton
    popular_query: KeyboardButton
    search_by_popular_query: KeyboardButton
    follow: KeyboardButton
    unfollow: KeyboardButton
    skip: KeyboardButton


KEYBOARD_DICT = KeyboardDict(
    search=KeyboardButton('Поиск позиции'),
    popular_query=KeyboardButton('Популярные запросы'),
    search_by_popular_query=KeyboardButton('Поиск по популярному запросу'),
    follow=KeyboardButton('Подписаться на рассылку позиций'),
    unfollow=KeyboardButton('Отписаться от рассылки позиций'),
    skip=KeyboardButton('Пропустить')

)


BOT_MAIN_MENU = ReplyKeyboardMarkup(
    [
        [
            KEYBOARD_DICT['search'].text,
            KEYBOARD_DICT['popular_query'].text,
        ],
        [
            KEYBOARD_DICT['search_by_popular_query'].text,
        ],
        [
            KEYBOARD_DICT['follow'],
        ]

    ],
    resize_keyboard=True,
)

SKIP_MENU = ReplyKeyboardMarkup(
    [
        [
            KEYBOARD_DICT['skip'].text,
        ],
    ],
    resize_keyboard=True,
)
