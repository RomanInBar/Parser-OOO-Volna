import csv
import logging

from utils.abstractions import AbstractStorage
from utils.exceptions import RepeatError


class Storage(AbstractStorage):
    """Работа с хранилищем данных."""
    def write(self, path: str, data: list[str]) -> None:
        if self.search(path, data):
            raise RepeatError
        """Записывает новые данные в хранилище."""
        with open(path, 'a', newline='', encoding='utf8') as f:
            csv.writer(f, delimiter=';').writerow(data)
            logging.info(f'Добавлены новые данные "{data}"')

    def read(self, path: str) -> list[list[str]]:
        """Выгружает все данные из хранилища."""
        with open(path, 'r', encoding='utf8') as f:
            data = [row for row in csv.reader(f, delimiter=';')]
            logging.info('Данные из хранилища загружены')
            return data

    def delete(self, path: str, index: int) -> None:
        """Удаляет данные из хранилища."""
        data: list = self.read(path)
        removed_item = data.pop(index)
        logging.info(f'Из файла "{path}" удален элемент "{removed_item}"')
        self.overwrite(path, data)

    def overwrite(self, path: str, data: list[list[str]]) -> None:
        """Перезаписывает данные хранилища."""
        with open(path, 'w', newline='', encoding='utf8') as f:
            csv.writer(f, delimiter=';').writerows(data)
            logging.info('Данные хранилища перезаписаны')

    def search(self, path: str, data: list[str]) -> bool:
        with open(path, 'r', encoding='utf8') as f:
            reader = csv.reader(f, delimiter=';')
            result = bool(row for row in reader if row == data)
            return result
