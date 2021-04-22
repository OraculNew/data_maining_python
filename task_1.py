"""Источник: https://5ka.ru/special_offers/
Задача организовать сбор данных,
необходимо иметь метод сохранения данных в .json файлы
результат: Данные скачиваются с источника, при вызове метода/функции сохранения в файл скачанные данные сохраняются в
Json вайлы, для каждой категории товаров должен быть создан отдельный файл и содержать товары исключительно
соответсвующие данной категории.
пример структуры данных для файла:
нейминг ключей можно делать отличным от примера

{
"name": "имя категории",
"code": "Код соответсвующий категории (используется в запросах)",
"products": [{PRODUCT}, {PRODUCT}........] # список словарей товаров соответсвующих данной категории
}"""

import json
import time
from pathlib import Path
import requests


class Parse5ka:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    params = {
        "records_per_page": 20,
        'categories': None
    }

    def __init__(self, star_url: str, save_path: Path):
        self.star_url = star_url
        self.save_path = save_path

    def _get_response(self, url, *args, **kwargs):
        while True:
            # не верные ссылки в json файлах заменяем на верные
            url = url.replace('http://monolith', 'https://5ka.ru')
            response = requests.get(url, *args, **kwargs)
            if response.status_code == 200:
                return response
            time.sleep(3)

    def run(self):
        n = 0
        for categories in self._parse(self.star_url, False):
            n += 1
            print(f'Загрузка данных по категории {n}. {categories["parent_group_name"]}')
            url = f"https://5ka.ru/api/v2/special_offers/"
            self.params['categories'] = categories['parent_group_code']
            items = []
            for itm in self._parse(url, True):
                items = items + itm
            catalog = {'id_categories': categories['parent_group_code'],
                            'name_categories': categories['parent_group_name'],
                            'items': items}
            file_path = self.save_path.joinpath(f"{categories['parent_group_code']}.json")
            self._save(catalog, file_path)

    def _parse(self, url: str, is_items):
        while url:
            time.sleep(0.1)
            response = self._get_response(url, headers=self.headers, params=self.params)
            data = response.json()
            if is_items is True:
                url = data["next"]
                yield data["results"]
            else:
                url = None
                for categories in data:
                    yield categories

    def _save(self, data: dict, file_path):
        file_path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')


def get_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


if __name__ == "__main__":
    save_path = get_save_path("products")
    url = "https://5ka.ru/api/v2/categories/"
    parser = Parse5ka(url, save_path)
    parser.run()
    print('end parsing')
