import logging

from utils.constants import PAHT_TO_LOGFILE, PATH_TO_STORAGE, PATH_TO_URLS, URL_FLAG, STORAGE_FLAG
from utils.exceptions import StorageFileNotFound, UrlsFileNotFound
from ginterface.gui import GInterface
from parser.parser import Parser
from database.storage import Storage


logging.basicConfig(
    level=logging.INFO,
    filename=PAHT_TO_LOGFILE,
    filemode='w',
    format='''%(levelname)s [%(asctime)s]: %(filename)s > %(funcName)s
    >>> %(message)s''',
    encoding='utf8'
)


def create_storage_files(flag: str):
    if flag == STORAGE_FLAG:
        with open(PATH_TO_STORAGE, 'w'): ...
    elif flag == URL_FLAG:
        with open(PATH_TO_URLS, 'w'): ...
    else:
        logging.exception(f'Невалидное имя флага: "{flag}"')


def check_files(storage: Storage):
    try:
        data = storage.read(PATH_TO_STORAGE)
        urls = sum(storage.read(PATH_TO_URLS), [])
    except StorageFileNotFound as error:
        logging.exception('File not found', exc_info=error)
        create_storage_files(STORAGE_FLAG)
        data = None
    except UrlsFileNotFound as error:
        logging.exception('File not found', exc_info=error)
        create_storage_files(URL_FLAG)
        urls = []
    return data, urls


def create_dict_structure(replace_words: list[list[str]]) -> dict[str, str]:
    """Переделывает структуру данных из хранилища."""
    try:
        new_structure = {old: new for [old, new] in replace_words}
        logging.info('Данные помещены в словарь')
    except ValueError:
        logging.info('Нет данных для замены')
        new_structure = {}
    finally:
        return new_structure


def main():
    queue = list()
    storage = Storage()
    data, urls = check_files(storage)
    data = create_dict_structure(data)
    parser = Parser(urls, data, queue)
    gui = GInterface(parser, storage, queue)
    gui.mainloop()


if __name__ == '__main__':
    main()
