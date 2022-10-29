"""Module for getting popular queries from trending-searches.wb.ru."""

import requests


def get_popular_query(query):
    url = f'https://trending-searches.wb.ru/api?itemsPerPage=100&offset=0&period=week&query={query}&sort=desc'
    r = requests.get(url=url)
    queries_info = r.json()['data']['list']
    return queries_info
