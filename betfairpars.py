from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

class BetfairParser:
    def __init__(self):
        self.page = 'https://www.betfair.com/exchange/plus/ru/%D1%84%D1%83%D1%82%D0%B1%D0%BE%D0%BB-%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%D1%8C-1'
        self.browser = None

    def browser_launch(self):
        options = Options()
        options.headless = False
        driver = webdriver.Firefox(options=options)
        return driver

    def get_online_game(self):
        if not self.browser:
            self.browser = self.browser_launch()
        self.browser.get(self.page)
        card_content = None
        while not card_content:
            print('[INFO] Ожидаем полную загрузку страницы')
            content = self.browser.page_source
            soup = BS(content, 'html.parser')
            card_content = soup.select('.card-content')
        print('[INFO] Страница загружена')
        print('[INFO] Сортируем по времени')
        combobox = self.browser.find_element_by_css_selector('.selected-option')
        combobox.click()
        option_list_items = self.browser.find_elements_by_css_selector('.option-list-item')
        for item in option_list_items:
            if item.text == 'Время':
                item.click()
                break
        li_name = []
        while len(li_name) < 3:
            print('[INFO] Ожидаем полную загрузку страницы')
            content = self.browser.page_source
            soup = BS(content, 'html.parser')
            li_name = soup.select('li.name')
        content = self.browser.page_source
        soup = BS(content, 'html.parser')
        tables = soup.select('.coupon-table.ng-scope')
        table_online_game = None
        for table in tables:
            if 'По ходу игры' in table.select('.ng-binding.ng-scope.ng-isolate-scope.large')[0].text:
                table_online_game = table
                break
        if table_online_game:
            time.sleep(1)
            table_online_game.select('.mod-event-line.ng-scope.ng-isolate-scope.large')

parser = BetfairParser()
parser.get_online_game()