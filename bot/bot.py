from constants import BOT_MAIN_MENU, TELEGRAM_TOKEN
from telegram import Bot
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater

import utils.position as position
from db.db import session
from db.repositories import user_queries_repository, user_repository
from utils.werocket.get_by_inside_article import get_article_by_inside_article

bot = Bot(token=TELEGRAM_TOKEN)


def start(update, context):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    user = user_repository.create(chat_id, username, first_name, last_name)
    session.commit()
    update.message.reply_text('Hello, {}!'.format(user.first_name), reply_markup=BOT_MAIN_MENU)


def help(update, context):
    update.message.reply_text('Help!')


def search(update, context):
    update.message.reply_text(
        'Введите артикул, поисковой запрос  и адресса (один или несколько) разделяя их абзацем! (Enter)'
        '\nПример: \n123456'
        '\nКроссовки\n'
        'Москва, ул. Ленина, д. 1')
    return 'get_query_and_send_position'


def get_query_and_send_position(update, context):
    try:
        article, query, *addresses = update.message.text.split('\n')

        article, query = article.strip(), query.strip()
        addresses = [address.strip() for address in addresses if address.strip()]
        try:
            article = int(article)
        except ValueError:
            article = int(get_article_by_inside_article(article))

        context.user_data['article'] = article
        context.user_data['query'] = query
        context.user_data['addresses'] = addresses
    except Exception as e:
        update.message.reply_text('Неверный формат ввода! Ошибка: {}'.format(e))
        return cancel(update, context)
    return send_position(update, context)


def cancel(update, context):
    update.message.reply_text('Поиск отменен!', reply_markup=BOT_MAIN_MENU)
    context.user_data.clear()
    return ConversationHandler.END


def send_position(update, context):
    query = context.user_data['query']
    article = context.user_data['article']
    addresses = context.user_data['addresses']
    result = {adress: position.get_position(query, adress, article) for adress in addresses}
    msg = ''
    for address, pos in result.items():
        msg += '{}: {}\n'.format(address, pos)
        user_queries_repository.create(
            user_id=update.message.chat_id,
            query=query,
            article=article,
            address=address,
            position=pos)
        user_queries_repository.commit()
    update.message.reply_text(msg, reply_markup=BOT_MAIN_MENU)
    return ConversationHandler.END


get_position_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(['Поиск']), search)],
    states={
        'get_query_and_send_position': [MessageHandler(Filters.text, get_query_and_send_position)],
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
