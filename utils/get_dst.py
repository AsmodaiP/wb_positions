import requests


def get_dst(address, longitude, latitude):
    url = 'https://www.wildberries.ru/webapi/geo/saveprefereduserloc'
    json_data = {
        'address': address,
        'longitude': longitude,
        'latitude': latitude
    }
    headers = {
        'x-requested-with': 'XMLHttpRequest',
    }

    response = requests.post(url, headers=headers, data=json_data)
    coocie_list = response.headers['Set-Cookie'].split(';')
    for cookie in coocie_list:
        if 'dst' in cookie:
            return cookie.split('=')[2].split('_')
    return


def get_coordinate_by_address(address):
    url = 'https://geocode-maps.yandex.ru/1.x/'
    params = {
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
        'geocode': address,
        'format': 'json'
    }
    response = requests.get(url, params=params)
    json_response = response.json()
    featureMember = json_response['response']['GeoObjectCollection']['featureMember'][0]
    longitude, latitude = featureMember['GeoObject']['Point']['pos'].split(' ')
    return {
        'longitude': longitude,
        'latitude': latitude
    }
