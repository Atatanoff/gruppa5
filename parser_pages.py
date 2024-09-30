from typing import Dict
import time
import random
from tqdm import tqdm
from playwright.async_api import Page
from playwright.sync_api import Playwright, sync_playwright
from links_for_pars import links_for_pars
from locators import selectors
from logger import logger
from setting import TIME_DELAY
from i18n import localec

class ParserSearchPage:
    def __init__(self, headless = True, verbose = True) -> None:
        self.t1, self.t2 = TIME_DELAY
        self.page = None
        self.context = None
        self.browser = None
        self.verbose = True
        self.head = headless
        self.ip_link_dict = dict()
        self.ip_indx = None

    def setup(self):
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=self.head)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def close(self):
        self.page.close()
        self.context.close()
        self.browser.close()

    def get_ip_by_number(self, indx=1):
        self.page.goto(self.ip_link_dict[self.ip_indx[int(indx)]])
        self.page.locator('//*[@id="right-data-company"]/div/div[2]/div[1]/div/div[1]/div/div').wait_for()
        data = {
                                      #//*[@id="right-data-company"]/div/div[1]/div[1]/div/div[1]/div[1]/div/h2
        "Название": self.page.locator('div.tpanel-header-content > div > h2').inner_text(),
        "ОГРН": self.page.locator('//*[@id="right-data-company"]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/span[1]').inner_text(),
        "ИНН": self.page.locator('//*[@id="right-data-company"]/div/div[1]/div[2]/div/div[2]/div[1]/div[2]/span[1]').inner_text(),
        "КПП": self.page.locator('//*[@id="right-data-company"]/div/div[1]/div[2]/div/div[2]/div[1]/div[2]/span[2]').inner_text(),
        "Дата регистрации": self.page.locator('//*[@id="right-data-company"]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/span[2]').inner_text(),
        }
        located = self.page.locator('//*[@id="right-data-company"]/div/div[1]/div[1]/div/div[2]/div/div[6]/div[2]')
        adress = self.page.locator('//*[@id="right-data-company"]/div/div[1]/div[2]/div/div[2]/div[4]/div/p[2]/span[1]')
        if located.is_visible():
            data['Местоположение'] = located.inner_text()
        if adress.is_visible():
            data['Юридический адрес'] = adress.inner_text()
        return data

    def run(self):
        if self.verbose:logger.info("Старт программы")
        if self.verbose:
            logger.info(localec.time_delay['ru'] % (self.t1, self.t2))
        self.setup()
        if self.verbose:logger.info(localec.load_page['ru'])
        self.page.goto(self.links_page_data)
        self.page.locator(selectors.mark_element).wait_for()
        if self.verbose:logger.info(localec.get_links["ru"])
        self.update_ip_link_dict()
        self.ip_indx = {i: k for i, k in enumerate(self.ip_link_dict)}

    def set_search_data(self, data: str):
        if not data: logger.error(localec.error_empty_data)
        self.links_page_data = links_for_pars.search_link + '%20'.join(data.split(' '))

    def get_links(self, links) -> Dict[str, str]:
        dict_links_ip = dict()
        links = tqdm(links) if self.verbose else links
        for el in links:
            dict_links_ip[el.inner_text()] = links_for_pars.main_link + el.get_attribute('href')
        return dict_links_ip

    def update_ip_link_dict(self):
        self.delay()
        a = self.page.locator(selectors.li_a_locator).all()
        if not a:
            links_el = self.page.locator(selectors.found_links).all()
            self.ip_link_dict.update(self.get_links(links_el))
            return
        flag = False
        for el in a:
            if el.inner_text() == "«":
                flag = True
                continue
            elif flag and el.inner_text() == "...":
                flag = False
                continue
            elif el.inner_text() == "...":
                el.click()
                self.update_ip_link_dict()
                return
            elif el.inner_text() == "»":
                break
            flag = False
            el.click()
            self.delay()
            links_el = self.page.locator(selectors.found_links).all()
            self.ip_link_dict.update(self.get_links(links_el))

    def delay(self):
        time.sleep(random.uniform(self.t1, self.t2))
