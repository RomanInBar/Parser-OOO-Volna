from bs4 import BeautifulSoup as bs
import re
import openpyxl
import requests
from utils.abstracts import AbstractParser
import logging


class Parser(AbstractParser):
    """Основные команды парсера."""
    def __init__(self, urls: list[str]) -> None:
        self.urls = urls

    def _request(self, url: str) -> str:
        """Запрос к url адресу."""
        response = requests.get(url)
        logging.info(f'Завершен запрос к url {url}. Статус: {response.status_code}')
        return response.text
    
    def scraping(self, html: str) -> bs:
        """Cкрапинг url страницы."""
        soup = bs(html, 'html.parser')
        return soup

    def start(self) -> list[bs]:
        """Запускает программы запроса и скрапинга url страницы."""
        responses = [self._request(url) for url in self.urls]
        soupes = [self.scraping(html) for html in responses]
        logging.info('Скрапинг всех url адресов завершен')
        return soupes
    

class DataProcessor:
    """Обработка полученных данных."""
    def get_carts_of_products(self, soup: bs) -> list[str]:
        """Получить все блоки карточек товаров со страниц."""
        cards = soup.find_all(attrs={'class': 'product-item'})
        logging.info('Карточки продуктов со страницы получены')
        return cards

    def extract_digit(self, string: str) -> str:
        """Вывести цифру из строки."""
        num = re.findall(r'\d+', string)[0]
        logging.info('Количество товара получено')
        return num

    def get_data_from_card(self, card: bs) -> list[str]:
        """Получить название и количество из карточки товара."""
        try:
            name = card.find(attrs={'class': 'product-item-title'}).text.strip()
            logging.info('Название товара получено')
        except Exception:
            logging.exception('Возникла ошибка при получении названия товара')
            name = 'None'
        try:
            data = card.find(attrs={'class': 'product-item-quantity'}).text.strip()
            quantity = self.extract_digit(data)
            logging.info('Данные о количестве получены')
        except Exception:
            logging.exception('Возникла ошибка при колучении данных о количестве')
            quantity = '0'
        logging.info('Получены данные о товаре')
        return [name, quantity]
    

class ChangeNames:
    """Замена слова в названии."""
    def __init__(self, new_names: dict[str, str]) -> None:
        self.new_names = new_names

    def split_words(self, string: str) -> list[str]:
        """Разделить название товара на список из слов."""
        logging.info('Название товара разделно на список слов')
        return string.split(' ')

    def change_name(self, name: str) -> str:
        """Меняет слово в названии, если оно есть в списке для замены."""
        if self.new_names.get(name):
            new_name = self.new_names[name]
            logging.info(f'Слово "{name}" заменено на "{new_name}"')
            return new_name
        return name
        
    def join_string(self, arr: list[str]) -> str:
        """Делает из списка слов строку."""
        return ' '.join(arr)
        
    
class FileManagerXML:
    """Команды для работы с итоговым файлом."""
    def __init__(self, titles: tuple[str], data: list[list[str]]) -> None:
        self.titles = titles
        self.data = data

    def create_file(self) -> None:
        """Создать новый xlsx файл."""
        self.wb = openpyxl.Workbook()
        logging.info('XLSX: Файл создан')

    def init_work(self) -> None:
        """Инициализирует работу с файлом."""
        self.sheet = self.wb.active

    def add_titles(self) -> None:
        """Добавляет заголовки в файл."""
        self.sheet.append(self.titles)
        logging.info('XLSX: Заголовки добавлены')

    def add_data(self) -> None:
        """Записывает скаченные данные в файл."""
        for item in self.data:
            self.sheet.append(tuple(item))
        logging.info('XLSX: Все данные записаны')

    def save_book(self, path) -> None:
        """Сохраняет файл."""
        self.wb.save(path)
        logging.info('XLSX: Файл сохранен')
    

class StartParser:
    """Команды для запуска парсера."""
    def __init__(self, urls: list, new_names: dict, path_save_file: str) -> None:
        self.new_names = new_names
        self.urls = urls
        self.data = []
        self._titles = ('Название', 'Количество')
        self.path = path_save_file

    def start(self):
        """Старт работы парсера."""
        self.init_tools()
        soup_urls = self.parser.start()
        cards = [self.processor.get_carts_of_products(soup) for soup in soup_urls]
        cards = sum(cards, [])
        for card in cards:
            name, quantity = self.processor.get_data_from_card(card)
            arr_words = self.changing.split_words(name)
            check_replace = [self.changing.change_name(name) for name in arr_words]
            name = self.changing.join_string(check_replace)
            self.data.append([name, quantity])
        self.create_file()
        logging.info('Работа парсера завершена')

    def init_tools(self):
        """Инициализация необходимых инструментов для работы парсера."""
        self.parser = Parser(self.urls)
        self.processor = DataProcessor()
        self.changing = ChangeNames(self.new_names)
        self.creatorfile = FileManagerXML(self._titles, self.data)
        logging.info('Все инструменты для работы парсера готовы.')

    def create_file(self):
        """Создает итоговый файл."""
        self.creatorfile.create_file()
        self.creatorfile.init_work()
        self.creatorfile.add_titles()
        self.creatorfile.add_data()
        self.creatorfile.save_book(self.path)
        logging.info('Итоговый файл готов')
