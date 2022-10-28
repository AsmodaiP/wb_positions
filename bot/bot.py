from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# from db.db import session
# from db.repositories import UserRepository
# from constants import TOKEN
import datetime
from db.repositories import TelegramUserRepository
from db.db import session
from constants import TELEGRAM_TOKEN, BOT_MAIN_MENU, SKIP_MENU
import utils.position as position

bot = Bot(token=TELEGRAM_TOKEN)


def start(update, context):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name

    user = TelegramUserRepository(session).create(chat_id, username, first_name, last_name)
    session.commit()
    update.message.reply_text('Hello, {}!'.format(user.first_name), reply_markup=BOT_MAIN_MENU)


def help(update, context):
    update.message.reply_text('Help!')




def search(update, context):
    update.message.reply_text('Введите поисковой запрос!')
    return 'get_query'


def get_query(update, context):
    query = update.message.text
    context.user_data['query'] = query
    update.message.reply_text('Введите артикул!')
    return 'get_article'

def cancel(update, context):
    update.message.reply_text('Поиск отменен!', reply_markup=BOT_MAIN_MENU)
    context.user_data.clear()
    return ConversationHandler.END

def get_article(update, context):
    try:
        article = int(update.message.text)
    except ValueError:
        update.message.reply_text('Неверный формат артикула!')
        return cancel()
    context.user_data['article'] = article
    update.message.reply_text('Введите адресс!', reply_markup=SKIP_MENU)
    return 'get_address'


def get_address(update, context):
    address = update.message.text
    context.user_data['address'] = address
    return send_position(update, context)


def send_position(update, context):
    print('send_position')
    pos= position.get_position(context.user_data['query'], context.user_data['address'], context.user_data['article'])
    update.message.reply_text('Позиция: {}'.format(pos), reply_markup=BOT_MAIN_MENU)
    return ConversationHandler.END


get_position_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(['Поиск']), search)],
    states={
        'get_query': [MessageHandler(Filters.text, get_query)],
        'get_article': [MessageHandler(Filters.text, get_article)],
        'get_address': [MessageHandler(Filters.text, get_address)],
        'send_position': [MessageHandler(Filters.text, send_position)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

        

updater = Updater(token=TELEGRAM_TOKEN)
for command, handler in [
    ('start', start),
    ('help', help),
]:
    updater.dispatcher.add_handler(CommandHandler(command, handler))

updater.dispatcher.add_handler(get_position_conversation)
updater.start_polling()
updater.idle()
