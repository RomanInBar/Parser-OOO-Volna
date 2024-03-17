from abstracts import AbstractDatabseCSV, AbstractServices


class Services(AbstractServices):
    def __init__(self, db) -> None:
        self._db: AbstractDatabseCSV = db

    def add_value(self, values: list[str]):
        self._db.write(values)

    def get_all_data(self) -> list[list[str]]:
        data = self._db.read()
        return data
    
    def delete_value(self, index: str):
        self._db.delete(int(index))
