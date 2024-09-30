from dataclasses import dataclass
from typing import Dict



@dataclass
class Locales:
    start_text: Dict[str, str]
    get_links: Dict[str, str]
    time_delay: Dict[str, str]
    load_page: Dict[str, str]
    error_empty_data: Dict[str, str]

localec = Locales(
    {
        "ru": "Введите фамилию и/или имя\n"
    },
    {
        "ru": "Собираю ссылки..."
    },
    {
        "ru": "Технические паузы для имитации человека от %dс до %dс"
    },
    {
        "ru": "Гружу страницу..."
    }
    ,
    {
        "ru": "Отсутствуют данные для поиска. Используйте метод set_search_data(data) для установки где data данные для поиска через пробел"
    }
    )
