import csv
from utils.abstracts import AbstractDatabseCSV
from utils.constants import PATH_TO_SPARE_STORAGE
import logging


class DatabaseCSV(AbstractDatabseCSV):
    """Работает с csv файлом в качестве хранилища данных."""
    def __init__(self, filename: str) -> None:
        self.storage = filename
        self._spare_storage = PATH_TO_SPARE_STORAGE
    
    def write(self, data: list[str]) -> None:
        """Записывает данные в хранилище данных."""
        with open(self.storage, 'a', newline='', encoding='utf8') as f:
            w = csv.writer(f, delimiter=';')
            w.writerow(data)
            self._data_migration(self.storage, self._spare_storage)
            logging.info(f'Добавлена запись "{data}" в хранилище')

    def overwrite(self, data: list[list[str]]) -> None:
        """Перезаписывает хранилище данных."""
        with open(self.storage, 'w', newline='', encoding='utf8') as f:
            w = csv.writer(f, delimiter=';')
            w.writerows(data)
            logging.info('Хранилище данных перезаписано')

    def read(self) -> list[list[str]]:
        """Считывает и возвращает информацию из хранилища данных."""
        with open(self.storage, 'r', encoding='utf8') as f:
            data = [row for row in csv.reader(f, delimiter=';')]
            logging.info('Данные прочитаны из хранилища')
            return data
        
    def delete(self, index: int) -> None | str:
        """Удаляет данные из хранилища."""
        rows = self.read()
        deleted_item = rows.pop(index)
        self.overwrite(rows)
        self._data_migration(self.storage, self._spare_storage)
        logging.info(f'Удалены данные "{deleted_item}"')

    def check_storage(self) -> None:
        """Проверка целостности данных хранилища."""
        logging.info('Проверка целостности данных хранилища')
        values = self.read()
        if not values:
            logging.exception('Выявлено повреждение данных основного хранилища. Инициализация переноса данных из запасного хранилища')
            self._data_migration(self._spare_storage, self.storage)
            logging.warning('Произведена миграция данных из запасного хранилища')
        else:
            logging.info('Целостность хранилища не нарушена')

    def _data_migration(self, file_from: str, file_to: str) -> None:
        with open(file_from, 'r', encoding='utf8') as f:
            relevant_data = [row for row in csv.reader(f, delimiter=';')]
        with open(file_to, 'w', newline='', encoding='utf8') as f:
            csv.writer(f, delimiter=';').writerows(relevant_data)
        
