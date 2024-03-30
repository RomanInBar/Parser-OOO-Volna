from utils.constants import PATH_TO_URLS, PATH_TO_STORAGE


class StorageFileNotFound(Exception):
    def __call__(self):
        return f'Файл "{PATH_TO_STORAGE}" не найден!'


class UrlsFileNotFound(Exception):
    def __call__(self):
        return f'Файл "{PATH_TO_URLS}" не найден!'


class ValuesNotFound(Exception):
    def __call__(self):
        return 'Данные не обнаружены!'
    

class RepeatError(Exception):
    def __call__(self):
        return 'Данные с таким значением уже записаны!'