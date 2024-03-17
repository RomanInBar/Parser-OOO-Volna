from bs4 import BeautifulSoup as bs
import re
import openpyxl
import requests


class QuantityError(Exception):
    pass


class Parser:
    def __init__(self, urls: list[str]) -> None:
        self.urls = urls

    def scraping(self, url: str) -> bs:
        response = requests.get(url).text
        soup = bs(response, 'html.parser')
        return soup

    def start(self) -> list[bs]:
        responses = [self.scraping(url) for url in self.urls]
        return responses
    

class DataProcessor:
    def get_carts_of_products(self, soup: bs) -> None:
        self.cards = soup.find_all(attrs={'class': 'product-item'})

    def extract_digit(self, string: str) -> str:
        num = re.findall(r'\d+', string)[0]
        return num

    def get_data_from_card(self, card: bs) -> list[str]:
        try:
            name = card.find(attrs={'class': 'product-item-title'}).text.strip()
        except Exception:
            name = 'None'
        try:
            data = card.find(attrs={'class': 'product-item-quantity'}).text.strip()
            quantity = self.extract_digit(data)
        except Exception:
            quantity = '0'
        return [name, quantity]
    

class ChangeNames:
    def __init__(self, new_names: dict[str, str]) -> None:
        self.new_names = new_names

    def split_words(self, string: str) -> list[str]:
        return string.split(' ')

    def change_name(self, name: str) -> str:
        if self.new_names.get(name):
            new_name = self.new_names[name]
            return new_name
        return name
        
    def join_string(self, arr: list[str]) -> str:
        return ' '.join(arr)
        
    
class FileManagerXML:
    def __init__(self, titles: tuple[str], data: list[list[str]]) -> None:
        self.titles = titles
        self.data = data

    def create_file(self) -> None:
        self.wb = openpyxl.Workbook()

    def init_work(self) -> None:
        self.sheet = self.wb.active

    def add_titles(self) -> None:
        self.sheet.append(self.titles)

    def add_data(self) -> None:
        for item in self.data:
            self.sheet.append(tuple(item))

    def save_book(self, path) -> None:
        self.wb.save(path)
    

class StartParser:
    def __init__(self, urls: list, new_names: dict, path_save_file: str) -> None:
        self.new_names = new_names
        self.urls = urls
        self.data = []
        self._titles = ('Название', 'Количество')
        self.path = path_save_file

    def start(self):
        self.init_tools()
        soup_urls = self.parser.start()
        [self.processor.get_carts_of_products(soup) for soup in soup_urls]
        for card in self.processor.cards:
            name, quantity = self.processor.get_data_from_card(card)
            arr_words = self.changing.split_words(name)
            check_replace = [self.changing.change_name(name) for name in arr_words]
            name = self.changing.join_string(check_replace)
            self.data.append([name, quantity])
        self.create_file()

    def init_tools(self):
        self.parser = Parser(self.urls)
        self.processor = DataProcessor()
        self.changing = ChangeNames(self.new_names)
        self.creatorfile = FileManagerXML(self._titles, self.data)

    def create_file(self):
        self.creatorfile.create_file()
        self.creatorfile.init_work()
        self.creatorfile.add_titles()
        self.creatorfile.add_data()
        self.creatorfile.save_book(self.path)
