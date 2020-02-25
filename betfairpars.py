from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time


class BetfairParser:
    def __init__(self):
        self.main_page = 'https://www.betfair.com/exchange/plus/'
        self.football_page = self.main_page + 'football'
        self.browser = None

    def browser_launch(self):
        options = Options()
        options.headless = False
        driver = webdriver.Firefox(options=options)
        return driver

    def get_games(self):
        if not self.browser:
            self.browser = self.browser_launch()
        self.browser.get(self.football_page)
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
        while len(li_name) != 100:
            print('[INFO] Ожидаем полную загрузку страницы')
            content = self.browser.page_source
            soup = BS(content, 'html.parser')
            li_name = soup.select('li.name')
        time.sleep(4)
        content = self.browser.page_source
        soup = BS(content, 'html.parser')
        tables = soup.select('.coupon-table-mod')
        games_info = []
        for table in tables:
            games = table.select('.mod-link')
            for game in games:
                game_info = {}
                command1 = game.select('.name')[0].text
                print(command1)
                command2 = game.select('.name')[1].text
                print(command2)
                time_match = game.select('.middle-label.ng-binding.ng-scope')
                if time_match:
                    game_info['in_play'] = True
                    time_match = game.select('.middle-label.ng-binding.ng-scope')[0].text
                    score1 = game.select('.ng-binding.ng-scope.home')[0].text
                    score2 = game.select('.ng-binding.ng-scope.away')[0].text
                    game_info['score1'] = score1
                    game_info['score2'] = score2
                else:
                    game_info['in_play'] = False
                    time_match = game.select('span.label')[0].text
                    print(time_match)
                link = game['href']
                print(link)
                game_info['command1'] = command1
                game_info['command2'] = command2
                game_info['time'] = time_match
                game_info['link'] = link
                games_info.append(game_info)
        print(games_info)
        for game in games_info:
            self.browser.get(self.main_page+game['link'])
            live_stream_popup = None
            live_stream_href = None
            while not live_stream_popup or not live_stream_href:
                content = self.browser.page_source
                soup = BS(content, 'html.parser')
                live_stream_popup = soup.select('.live-stream-popup')
                if live_stream_popup:
                    try:
                        live_stream_href = live_stream_popup[0]['href']
                    except KeyError:
                        live_stream_href = None
            print(self.main_page+'pop-out-live-stream/'+live_stream_popup[0]['href'])
            #live_stream_page = live_stream_popup[0]['href']



parser = BetfairParser()
parser.get_games()