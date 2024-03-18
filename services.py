from utils.abstracts import AbstractDatabseCSV, AbstractServices
import logging


class Services(AbstractServices):
    """Набор команд для работы с хранилищем данных."""
    def __init__(self, db) -> None:
        self._db: AbstractDatabseCSV = db

    def add_value(self, values: list[str]):
        """Добавить запись."""
        logging.info('Инициализирую программу записи данных')
        if not self._data_validation(values):
            logging.warning('Новые данные не прошли валидацию')
        else:
            self._db.write(values)
        
    def get_all_data(self) -> list[list[str]]:
        """Получить все данные из хранилища."""
        logging.info('Инициализирую программу чтения данных')
        data = self._db.read()
        return data
    
    def delete_value(self, index: str):
        """Удалить запись из хранилища."""
        logging.info('Инициализирую программу удаления данных')
        self._db.delete(int(index))

    def _data_validation(self, data: list[str]) -> bool:
        try:
            assert data
            assert len(data) == 2
            assert data[0]
            assert data[1]
            return True
        except AssertionError:
            return False
