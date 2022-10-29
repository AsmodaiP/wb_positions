"""Module  with bot  handlers  and  commands."""

from constants import BOT_MAIN_MENU, TELEGRAM_TOKEN
from telegram import Bot, ParseMode
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater

import utils.position as position
from db.db import session
from db.repositories import user_queries_repository, user_repository
from utils.get_popular_query import get_popular_query
from utils.werocket.get_by_inside_article import get_article_by_inside_article

bot = Bot(token=TELEGRAM_TOKEN)


def add_user_to_db_if_not_exists(func):
    """Add user to db if not exists decorator."""
    def wrapper(update, context):
        chat_id = update.message.chat_id
        username = update.message.chat.username
        first_name = update.message.chat.first_name or ''
        last_name = update.message.chat.last_name or ''
        user_repository.create_or_update(chat_id, username, first_name, last_name)
        session.commit()
        return func(update, context)
    return wrapper


@add_user_to_db_if_not_exists
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Добро пожаловать в бота поиска позиций!', reply_markup=BOT_MAIN_MENU)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


@add_user_to_db_if_not_exists
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
    result = {}
    for address in addresses:
        pos = position.get_position(query, address, article)
        update.message.reply_text('Адрес: {}\nРезультат: {}'.format(address, pos))
        result[address] = pos
    msg = 'Результаты поиска: \n'
    for address, pos in result.items():
        msg += '{}:  {}\n'.format(address, pos)
        user_queries_repository.create(
            user_id=update.message.chat_id,
            query=query,
            article=article,
            address=address,
            position=pos)
        user_queries_repository.commit()
    update.message.reply_text(msg, reply_markup=BOT_MAIN_MENU)
    return ConversationHandler.END


def get_query(update, context):
    update.message.reply_text('Введите поисковой запрос')
    return 'get_query'


def get_position_conversation_start(update, context):
    update.message.reply_text('Введите артикул ')


def send_popular_query(update, context):
    query = update.message.text
    popular_query = get_popular_query(query)
    msg = 'Запрос: количество'
    for query in popular_query:
        if len(msg) + len(query) > 3000:
            update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=BOT_MAIN_MENU)
            return ConversationHandler.END
        msg += '\n<code>{}</code>: {}'.format(query['text'], query['requestCount'])

    update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=BOT_MAIN_MENU)
    return ConversationHandler.END


def get(update, context):
    context.user_data['query'] = update.message.text
    update.message.reply_text('Введите артикул')
    return 'get_article_and_send_position'


def get_more_popular_query(update, context):
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

    return send_more_popular_position(update, context)


def send_more_popular_position(update, context):
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

    queries = get_popular_query(query)[:10]
    result = {query['text']: {} for query in queries}
    for address in addresses:
        for query in queries:
            pos = position.get_position(query['text'], address, article)
            result[query['text']][address] = pos
            update.message.reply_text(
                'Адрес: {}\nЗапрос: {}\nРезультат: {}'.format(address, query['text'], pos))
        msg = 'Результаты поиска: \n Адрес: {}\n'.format(address)

    for address in addresses:
        msg = 'Результаты поиска: \n'
        msg += 'Адрес: {}\n'.format(address)
        for query in queries:
            msg += f'{query["text"]}: {result[query["text"]][address]}\n'
        update.message.reply_text(msg, reply_markup=BOT_MAIN_MENU)
    return ConversationHandler.END


get_position_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(['Поиск']), search)],
    states={
        'get_query_and_send_position': [MessageHandler(Filters.text, get_query_and_send_position)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

get_popular_query_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(['Популярные запросы']), search)],
    states={
        'get_query_and_send_position': [MessageHandler(Filters.text, get_more_popular_query)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)


search_more_popular_query_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(['Поиск по популярным запросам']), search)],
    states={
        'get_query_and_send_position': [MessageHandler(Filters.text, send_more_popular_position)],
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
updater.dispatcher.add_handler(get_popular_query_conversation)
updater.dispatcher.add_handler(search_more_popular_query_conversation)
updater.start_polling()
updater.idle()
