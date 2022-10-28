from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# from db.db import session
# from db.repositories import UserRepository
# from constants import TOKEN
from positi

bot = Bot(token='TOKEN')

def start(bot, update):
    user = UserRepository(session).create(
        chat_id=update.message.chat_id,
        username=update.message.chat.username,
        first_name=update.message.chat.first_name,
        last_name=update.message.chat.last_name,
    )
    session.commit()
    update.message.reply_text(f'Hello, {user.first_name}!')

def help(bot, update):
    update.message.reply_text('Help!')

