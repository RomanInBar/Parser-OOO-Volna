from utils.abstractions import AbstractParser, AbstractDataProcessor
from utils.constants import FILE_TITLES, SAVE_FINAL_FILE_TO
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup as bs
import logging
import re
import openpyxl
import requests
from types import GeneratorType


class Parser(AbstractParser):
    def __init__(self, urls: list[str], change_names: dict[str, str], queue: list) -> None:
        self.names = change_names
        self.urls = urls
        self.processor: AbstractDataProcessor = DataProcessor(self.names)
        self.final_file = FinalFile()
        self.queue = queue

    def scraping(self, url: str) -> str:
        """Отправляет GET запрос на указанный url, возвращает html код."""
        response = requests.get(url).content
        return response

    def create_soup(self, html: str) -> list[bs]:
        """Возвращает объект BeautifulSoup распарсенного html кода."""
        soup = bs(html, features='html.parser')
        return soup

    def get_data(self, cards: list[bs]) -> list[str]:
        """Возвращает данные [имя, количество] из карточки товара."""
        data = [
            self.processor.get_data_from_card(card) for card in cards
        ]
        return data

    def get_cards(self, page: bs) -> list[bs]:
        """Возвращает карточки продуктов со страницы."""
        cards = self.processor.get_carts_of_products(page)
        return cards

    def start_of_data_parsing(self) -> GeneratorType:
        """
        Создаёт пул потоков, инициализирует запросы к целевый адресам,
        запускает сбор данных со страниц.
        """
        with ThreadPoolExecutor(max_workers=10) as pool:
            responses_html = pool.map(self.scraping, self.urls)
            logging.info('HTML коды страниц получены')
            soup = pool.map(self.create_soup, responses_html)
            logging.info('HTML коды страниц распарсены')
            cards = pool.map(self.get_cards, soup)
            logging.info('Карточки продуктов получены')
            data = pool.map(self.get_data, cards)
            logging.info('Данные из карточек получены')
            return data

    def start(self):
        """Запускает работу парсера."""
        data = sum(self.start_of_data_parsing(), [])
        self.final_file.create(data)
        if self.queue:
            logging.info('Инициирую завершающий метод из "одчереди"')
            end = self.queue.pop()
            end()
        

class DataProcessor(AbstractDataProcessor):
    def __init__(self, new_names: dict) -> None:
        self.change_name = new_names

    def get_carts_of_products(self, page: bs) -> list[bs]:
        """Получить все блоки карточек товаров со страниц."""
        cards = page.find_all(attrs={'class': 'product-item'})
        logging.info('Карточки продуктов со страницы получены')
        return cards
    
    def extract_digit(self, string: str) -> str:
        """Вывести цифру из строки."""
        num = re.findall(r'\d+', string)[0]
        return num
    
    def get_data_from_card(self, card: bs) -> list[str]:
            """Получить название и количество из карточки товара."""
            try:
                name = card.find(attrs={'class': 'product-item-title'}).text.strip()
                split_name = name.split(' ')
                new_name = [self.change_name.get(word) or word for word in split_name]
                name = ' '.join(new_name)
                assert isinstance(name, str)
                logging.info('Название товара получено')
            except Exception as error:
                logging.exception('Возникла ошибка при получении названия товара', exc_info=error)
                name = 'None'
            try:
                data = card.find(attrs={'class': 'product-item-quantity'}).text.strip()
                quantity = self.extract_digit(data)
                assert quantity.isdigit()
                logging.info('Данные о количестве получены')
            except Exception:
                logging.exception('Возникла ошибка при колучении данных о количестве')
                quantity = '0'
            logging.info('Получены данные о товаре')
            return [name, quantity]


class FinalFile:
    def create(self, data: list[list[str]]):
        """Создаёт конечный файл с данными."""
        wb = openpyxl.Workbook()
        logging.info('[XLSX] Файл создан')
        sheet = wb.active
        sheet.append(FILE_TITLES)
        for item in data:
            sheet.append(tuple(item))
        logging.info('[XLSX] Данные добавлены')
        wb.save(SAVE_FINAL_FILE_TO)
        logging.info('[XLSX] Файл сохранен')
