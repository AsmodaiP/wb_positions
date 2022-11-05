import datetime

import utils.position as position
from bot import bot
from db.repositories import favorite_queries_repository, user_queries_repository
from utils.get_dst import get_dst


def send_notifications():
    """Send notifications to all users."""
    overdue_follows = favorite_queries_repository.get_all_with_overdue_date()
    for follow in overdue_follows:
        try:
            follow.date_to_notify = follow.date_to_notify + datetime.timedelta(days=1)
            query = follow.query
            address = query.address
            article = query.article
            user_id = follow.telegram_user_id

            dst = ','.join(get_dst(address))
            pos = position.get_position(query.query, dst, article)
            previous = user_queries_repository.get_last_position_by_query_and_address(query.query, address)
            user_queries_repository.create(
                user_id=user_id,
                query=query,
                article=article,
                address=address,
                position=pos,
                dst=dst)

            url = f'https://www.wildberries.ru/catalog/{article}/detail.aspx?targetUrl=XS'

            msg = 'Информация по подписке:\n'
            msg += f'Запрос: {query.query}\n'
            msg += f'Адрес: {address}\n'
            msg += f'Артикул: [{article}]({url}) \n'
            msg += f'Текущая позиция: {pos}\n'
            if previous:
                msg += f'Предыдущая позиция: {previous.position}\n'
                if pos != previous.position:
                    msg += f'Изменение: {pos - previous.position} { "🔝" if pos > previous.position else "🔻" }'
            else:
                msg += 'Предыдущая позиция: неизвестна'
            bot.send_message(user_id, msg, parse_mode='Markdown')
            user_queries_repository.commit()
        except Exception:
            # TODO log error
            pass


if __name__ == '__main__':
    send_notifications()
