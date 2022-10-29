import json

import requests

from db.repositories import pickup_repository


def get_position(query, address, target_id):
    pickup = pickup_repository.get_by_address(address)
    if pickup:
        dst = pickup.wb_dst
    else:
        pickup = pickup_repository.create_by_address(address)
        pickup_repository.commit()
        dst = pickup.wb_dst
    position = parser(query, dst, int(target_id))
    print((query, dst, target_id))
    return position


def parser(query, dst, target_id):
    page = 1
    position = 1
    flag = True
    headers = {
        "Accept": "*/*",
        "User-Agent": ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/103.0.5060.53 Safari/537.36')
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
            "&spp=0"
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
