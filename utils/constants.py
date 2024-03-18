import os


desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
ROOT = 'Parser-OOO-Volna'
PATH_TO_STORAGE = f'{ROOT}/database/storage.csv'
PATH_TO_URLS = f'{ROOT}/urls.txt'
RESULT_FILE_NAME = 'recieved_data.xlsx'
PATH_TO_RESULT_FILE = f'{desktop}/{RESULT_FILE_NAME}'
PATH_TO_LOG_FILE = f'{ROOT}/loges.log'
PATH_TO_SPARE_STORAGE = f'{ROOT}/database/spare_storage.csv'