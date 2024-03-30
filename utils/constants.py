import os
from datetime import datetime


desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
date = datetime.now().date()

ROOT = 'src'
STORAGE_NAME = 'storage.csv'
LOGFILE_NAME = 'loges.log'
FINAL_FILE = f'Данные от {date}.xlsx'
URLS_FILE = 'urls.csv'
FILE_TITLES = ('Название', 'Количество')

PATH_TO_STORAGE = f'{ROOT}/database/{STORAGE_NAME}'
PATH_TO_URLS = f'{ROOT}/database/{URLS_FILE}'
PAHT_TO_LOGFILE = f'{ROOT}/{LOGFILE_NAME}'
SAVE_FINAL_FILE_TO = f'{desktop}/{FINAL_FILE}'

URL_FLAG = 'url'
STORAGE_FLAG = 'storage'
