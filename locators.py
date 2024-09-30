from dataclasses import dataclass


@dataclass
class Locators:
    mark_element: str = '//*[@id="serach-filters-block"]/div[2]'
    found_links: str = '//*[@id="search_result"]/div/div/div/p[1]/a'
    ul_locator: str = '//*[@id="search_result"]/ul'
    li_a_locator:str = '//*[@id="search_result"]/ul/li/a'

selectors = Locators()
