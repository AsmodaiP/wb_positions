import json

import openpyxl
from get_popular_query import get_popular_query
from position import get_position
from tqdm import tqdm

from get_dst import get_dst


def parse_all_query(query, addresses, article):
    queries = get_popular_query(query)
    result = {query['text']: {} for query in queries}
    for address in addresses:
        dst = ','.join(get_dst(address))
        for query in tqdm(queries, desc='Поиск по address: {}'.format(address)):
            pos = get_position(query['text'], dst, article)
            result[query['text']][address] = pos
        with open('result.json', 'w') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
    return result


def dump_position_in_excel():
    with open('result.json', 'r') as f:
        result = json.load(f)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Запрос', 'Адрес', 'Позиция'])
    for i, query in enumerate(result):
        for address in result[query]:
            ws.append([query, address, result[query][address]])

    wb.save('result.xlsx')


if __name__ == '__main__':
    addresses = ['г. Москва, м Красные ворота, ул. Машкова, 16']
    article = 17290081
    query = 'гирлянда'
    result = parse_all_query(query, addresses, article)
    dump_position_in_excel()
