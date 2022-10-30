import asyncio
import json

import aiohttp


async def async_parser(query, dst, target_id, page=1, position=1, flag=True):
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
        async with aiohttp.ClientSession() as session:
            for page in range(1, 100):
                async with session.get(url=url, headers=headers) as r:
                    try:
                        products = (await r.json())['data']['products']
                        if len(products) > 0:
                            for product in products:
                                id = product['id']
                                if id == target_id:
                                    finded_position = position
                                    return finded_position
                                position += 1
                    except KeyError:
                        return None
                    except Exception:
                        flag = False
                    finally:
                        page += 1


async def async_get_position(query, page, dst, target):
    async with aiohttp.ClientSession() as client:
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
        data1 = await get_json(client, url)
        jn = json.loads(data1.decode('utf-8'))
        try:
            products = jn['data']['products']
            if len(products) > 0:
                for index, product in enumerate(products, start=1):
                    id = product['id']
                    if id == target:
                        return (page - 1) * 100 + index
            else:
                return None
        except KeyError:
            return None


async def get_json(client, url):
    attempt = 0
    while attempt < 30:
        try:
            async with client.get(url) as response:
                assert response.status == 200
                return await response.read()
        except Exception:
            pass


async def parse_position(query, dst, target_id):
    futures = [async_get_position(query, page,
                                  dst, target_id) for page in range(1, 100)]
    results = await asyncio.gather(*futures)
    for result in results:
        if result is not None:
            return result
    return None


def get_position(query, dst, target_id):
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = loop.run_until_complete(parse_position(query, dst, target_id))
    return result
