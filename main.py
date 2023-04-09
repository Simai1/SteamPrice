import json
import os

import requests

from math import ceil

headers = {
    "Accept-Language": "ru",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/110.0.0.0 YaBrowser/23.3.1.806 Yowser/2.5 Safari/537.36",
    "Cookie": f"steamLoginSecure={os.getenv('LOGIN_SECURE')}"
}


def get_dota_items(items_count: int) -> list:
    """Получает {items_count} первых предметов с торговой площадки
    отсортированных по популярности. Возвращается список предметов
    в виде [{'name', 'hash_name', 'sell_listings', 'sell_price', 'sell_price_text', 'app_icon'},...]
    """
    items = []
    if items_count < 0:
        raise Exception("Неверное кол-во предметов")
    items_count = ceil(items_count / 10) * 10
    url = "https://steamcommunity.com/market/search/render"
    sess.params = ({
        "count": 10,
        "norender": 1,
        "search_descriptions": 0,
        "sort_column": "popular",
        "sort_dir": "desc",
        "appid": 570
    })
    for i in range(0, items_count, 10):
        sess.params["start"] = i
        response = sess.get(url)
        json_dict = json.loads(response.text)
        for item in json_dict["results"]:
            items.append(item)
    return items


def main():
    items = get_dota_items(50)
    print(items[0])


if __name__ == '__main__':
    sess = requests.Session()
    sess.headers.update(headers)
    main()
