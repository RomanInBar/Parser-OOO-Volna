import logging

from utils.abstracts import AbstractServices, AbstractParser


class CommandsOfGUI:
    """Сборник команд для графического интерфейса."""
    def __init__(self, services: AbstractServices, parser: AbstractParser) -> None:
        self.services = services
        self.parser = parser

    def get_all_data(self):
        """Получить все данные из хранилища данных."""
        logging.info('Начинаю загрузку данных из хранилища')
        return self.services.get_all_data()
    
    def add_value(self, *args):
        """Добавить запись в хранилище данных."""
        logging.info('Начинаю добавление записи в хранилище данных.')
        self.services.add_value(*args)

    def delete_value(self, *args):
        """Удалить запись из хранилища данных."""
        logging.info('Начинаю удаление записи из хранилища данных')
        self.services.delete_value(*args)
        
    def init_start(self):
        """Инициализация работы парсера."""
        logging.info('Инициализирован запуск парсера')
        self.parser.start()
    