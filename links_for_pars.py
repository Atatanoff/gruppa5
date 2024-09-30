from dataclasses import dataclass


@dataclass
class Links:
    search_link: str = 'https://zachestnyibiznes.ru/search?query='
    main_link: str = 'https://zachestnyibiznes.ru'

links_for_pars = Links()
