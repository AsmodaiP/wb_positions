from db.scheme import TelegramUser, UserQueries, Positions, Base, PickUps

from db.repositories import PickUpsRepository, pickup_repository
from db.db import session
import json
import requests
from utils.get_dst import get_coordinate_by_address, get_dst


def get_position(query, address, target_id):
    pickup = pickup_repository.get_by_address(address)
    # if pickup:
    #     dst = pickup.wb_dst
    
    coordinate = get_coordinate_by_address(address)
    dst = get_dst(address, **coordinate)
    pickup_repository.create(address, coordinate['latitude'], coordinate['longitude'], dst)
    position = parser(query, ','.join(dst), target_id)
    return position


def parser(query, dst, target_id):
    page = 1
    position = 1
    flag = True
    headers = {
        "Accept": "*/*",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'
    }
    finded_position = None
    while flag:
        url = "https://search.wb.ru/exactmatch/ru/common/v4/search" \
            "?appType=1" \
            "&curr=rub" \
            f"&dest={dst}" \
            "&emp=0" \
            "&lang=ru" \
            "&locale=ru" \
            f"&page={page}" \
            "&pricemarginCoeff=1.0" \
            f"&query={query}" \
            "&reg=0" \
            "&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71" \
            "&resultset=catalog" \
            "&sort=popular" \
            "&spp=0" \
            "&stores=117673,122258,122259,125238,125239,125240,6159,507,3158,117501,120602,120762,6158,121709,124731,159402,2737,130744,117986,1733,686,132043,1193"
        if page < 500:
            r = requests.get(url=url, headers=headers)
            html_cod = r.text
            try:
                products = r.json()['data']['products']
                if len(products) > 0:
                    for product in products:
                        id = product['id']
                        if id == target_id:
                            finded_position = position
                            return finded_position
                        position += 1
            except KeyError:
                return None 
            except Exception as ex:
                print(f"ошибка {ex}")
                print(json.loads(html_cod))
                flag = False
            finally:
                page += 1


