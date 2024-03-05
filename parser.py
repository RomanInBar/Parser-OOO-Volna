import os
import re
import time
from datetime import datetime
from typing import Any, Iterable, Callable
from fake_useragent import UserAgent

import openpyxl
import requests
from bs4 import BeautifulSoup



def time_decor(func: Callable):
    """Декоратор, замеряющий время работы программы."""

    def wrapper(*args, **kwargs) -> None:
        start = time.time()
        func(*args, **kwargs)
        print(f'Время работы программы: {time.time() - start}')
        return

    return wrapper


def change_name(data: list[str], replacement: dict[str, str]) -> list[str]:
    """
    Принимает список значений data = [имя, кол-во],
    заменяет слово из имени на значение из словаря replacement.
    """
    name, quantity = data
    if replacement.get(name):
        name = replacement[name]
    return [name, quantity]


def get_data(product: BeautifulSoup) -> list[str]:
    """
    Принимает объект BeautifulSoup, xml код с карточкой продукта.
    Выбирает информацию о названии и оставшемся кол-ве.
    """
    name = product.find(attrs={'class': 'product-item-title'}).a.string
    try:
        quantity = product.find(
            attrs={'class': 'product-item-quantity'}
        ).string
        quantity = re.search(r'\d+', quantity).group()
    except AttributeError:
        quantity = '0'
    finally:
        return [str(name), quantity]


def get_products(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Принимает объект BeautifulSoup, xml код страницы.
    Выбирает информацию о карточках продуктов.
    """
    products = soup.find_all(attrs={'class': 'product-item'})
    return products


def scraping_url(url: str) -> BeautifulSoup:
    """
    Принимает url-адрес. Парсит страницу, html -> xml.
    """
    html_code = requests.get(url, headers={'user-agent': UserAgent().chrome}).content.decode('utf8')
    soup = BeautifulSoup(html_code, features='html.parser')
    return soup


def get_urls_from_file(filename: str) -> list[str]:
    """Выбирает url-адреса из файла."""
    with open(filename, 'r') as file:
        data = [row.rstrip() for row in file]
    return data


def get_names_from_file(filename: str) -> dict[str, str]:
    """
    Создаёт спискок с данными из файла.
    """
    data = {}
    with open(filename, 'r', encoding='utf8') as file:
        for row in file:
            row = row.rstrip().split(' ')
            data[str(row[0])] = str(row[1])
    return data


def iteration(func: Callable, data: Iterable, *args) -> list[Any]:
    """Функция-итератор."""
    new_data = [func(item, *args) for item in data]
    return new_data


def create_xl_file(data: list[tuple]) -> None:
    """Создает xl файл с полученными данными на рабочем столе."""
    wb = openpyxl.Workbook()
    date = datetime.now().date()
    sheet = wb.active
    sheet.append(('артикул', 'кол-во'))
    for items in data:
        sheet.append(tuple(items))
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    wb.save(f'{desktop}/Данные от {date}.xlsx')


@time_decor
def main() -> None:
    """Флагманская функция, запускает алгоритм работы программы."""
    urls = get_urls_from_file('urls.txt')
    replacement = get_names_from_file('new_name.txt')
    xml_files = iteration(scraping_url, urls)
    products_xml = sum(iteration(get_products, xml_files), [])
    products_data = iteration(get_data, products_xml)
    change_name_of_products = iteration(
        change_name, products_data, replacement
    )
    create_xl_file(change_name_of_products)


if __name__ == '__main__':
    main()
