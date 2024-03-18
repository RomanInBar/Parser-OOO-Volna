from database.db import DatabaseCSV
from services import Services
from gui.gui_commands import CommandsOfGUI
from gui.gui import GraphicInterface
from parserv import StartParser
from utils.constants import PATH_TO_STORAGE, PATH_TO_URLS, PATH_TO_RESULT_FILE, PATH_TO_LOG_FILE, PATH_TO_SPARE_STORAGE
import logging
import os


logging.basicConfig(
    level=logging.INFO,
    filename=PATH_TO_LOG_FILE,
    filemode='w',
    format='''%(levelname)s [%(asctime)s]: %(filename)s > %(funcName)s
    >>> %(message)s''',
    encoding='utf8'
)


class InitialisationProgramm:
    """Инициализация и подговтовка всех компонентов программы."""
    def __init__(self) -> None:
        pass

    def get_urls(self, path: str) -> list[str]:
        """Получить url адреса из файла."""
        with open(path, 'r', encoding='utf8') as file:
            urls = [row.strip() for row in file]
            logging.info('URL адреса получены')
            return urls

    def get_names(self, db: DatabaseCSV) -> dict[str, str]:
        """Получить данные из хранилища данных."""
        data = {old: new for [old, new] in db.read()}
        logging.info('Данные из хранилища получены, словарь значений сформирован')
        return data
            
    def init_db(self, path: str) -> DatabaseCSV:
        """Инициализация хранилища данных."""
        db = DatabaseCSV(path)
        logging.info('Инициализация хранилища данных завершена')
        return db

    def init_services(self, db: DatabaseCSV) -> Services:
        """Инициализация сервисов."""
        services = Services(db)
        logging.info('Инициализация сервисов завершена')
        return services

    def init_parser(self, urls: list[str], change_names: dict[str, str], path_save_file: str) -> StartParser:
        """Инициализация парсера."""
        parser = StartParser(urls, change_names, path_save_file)
        logging.info('Инициализация парсера завершена.')
        return parser

    def init_commangs(self, services: Services, parser: StartParser) -> CommandsOfGUI:
        """Инициализация сборника команд к графическому интерфейсу."""
        gui_commands = CommandsOfGUI(services, parser)
        logging.info('Инициализация сборника команд к графическому интерфейсу завершена')
        return gui_commands

    def init_app(self, commands: CommandsOfGUI) -> GraphicInterface:
        """Инициализация графического интерфейса."""
        app = GraphicInterface(commands)
        logging.info('Инициализация графического интерфейса завершена')
        return app
    

def check_files():
    files = []
    if not os.path.isfile(PATH_TO_URLS):
        raise FileNotFoundError
    if not os.path.isfile(PATH_TO_STORAGE):
        files.append(PATH_TO_STORAGE)
    if not os.path.isfile(PATH_TO_SPARE_STORAGE):
        files.append(PATH_TO_SPARE_STORAGE)
    for file in files:
        with open(file, 'w'):
            pass


def start_program():
    """Запуск программы"""
    init = InitialisationProgramm()
    db = init.init_db(PATH_TO_STORAGE)
    db.check_storage()
    servis = init.init_services(db)
    urls = init.get_urls(PATH_TO_URLS)
    names = init.get_names(db)
    parser = init.init_parser(urls, names, PATH_TO_RESULT_FILE) 
    gui_commands = init.init_commangs(servis, parser)
    app = init.init_app(gui_commands)
    logging.info('Все компоненты программы подготовлены. Запуск')
    app.mainloop()


def main():
    """Проверка необходимых файлов и старт программы."""
    try:
        check_files()
    except FileNotFoundError:
        logging.exception('Отсутствует файл с целевыми url адресами')
        return
    start_program()


if __name__ == '__main__':
    main()
