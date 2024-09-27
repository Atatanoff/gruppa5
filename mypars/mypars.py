import os
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import random


def parse_html(url):
        "#search_result > div:nth-child(3)"
        soup = BeautifulSoup(url, 'html.parser')
        #print(soup)
        search_result = soup.find(id='search_result')
        #print(type(search_result))

        digit = 0
        text_digit = search_result.find(id='block-curr-filters-1').text
        for i in text_digit.split():
            if i.isdigit():
                digit += int(i)
        print(digit)
        result_searching = {}
        try:
            for i in range(digit-1):

                div = search_result.find_all('div', 'background-grey-blue-light p-15 b-radius-5 m-b-20')[i]
                name_pars = div.find('a', 'no-underline-full').text.strip()
                link_pars = f"https://zachestnyibiznes.ru{div.find('a', 'no-underline-full')['href'].strip()}"
                result_searching[name_pars] = link_pars
        except:
             pass

        return result_searching

class TestLoginFromMainPage:

    def test_fill_fields(self, page) -> None:
        "https://zachestnyibiznes.ru/search?query=Иванов"
        "https://zachestnyibiznes.ru/search?query=Иванов%20Иван"
        names = input("Введите фамилию и имя")
        #names="Иванов"
        formatted_names = '%20'.join(names.split(' '))
        url = f'https://zachestnyibiznes.ru/search?query={formatted_names}'
        page.goto(url)
        for i in tqdm(range(100)):
            time.sleep(random.uniform(0.03, 0.4))
        #time.sleep(12)
        html = page.content()
        p = parse_html(html)
        #print(p)
        #s = page.locator('.background-grey-blue-light p-15 b-radius-5 m-b-20')
        #print(len(s))
        ids = False
        keys = list(p.keys())
        for idx, key in enumerate(keys, 1):
            print(f"{idx}. {key}")
        try:
            selected_index = int(input("Выберите номер нужного вам ключа: ")) - 1

            if 0 <= selected_index < len(keys):
                selected_key = keys[selected_index]
                ids = p[selected_key]
            else:
                print("Ошибка: введен неправильный номер.")

        except ValueError:
            print("Ошибка: введите число.")
        print(ids)
        if ids:

            page.goto(ids)
            for i in tqdm(range(100)):
                time.sleep(random.uniform(0.03, 0.4))
            #t = page.get_by_text("ИНДИВИДУАЛЬНЫЙ ПРЕДПРИНИМАТЕЛЬ").inner_text()
            t = page.locator('//*[@id="right-data-company"]/div/div[1]/div[11]/div/div[2]/p').inner_text().split()

            city = page.locator('//*[@id="right-data-company"]/div/div[1]/div[1]/div/div[2]/div/div[6]/div[2]').inner_text()

            print(' '.join(t[0:5]))
            print(' '.join(t[15:17]))
            print(' '.join(t[17:19]))
            print(' '.join(t[20:]))
            print(f'Город: {city}')


        # page.get_by_text("Подтвердить", exact=True).click()
