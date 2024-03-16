import csv
from abstracts import AbstractDatabseCSV


class DatabaseCSV(AbstractDatabseCSV):
    def __init__(self, filename: str) -> None:
        self.file = filename

    def write(self, data: list[str]) -> None:
        with open(self.file, 'a', newline='', encoding='utf8') as file:
            w = csv.writer(file, delimiter=';')
            w.writerow(data)

    def overwrite(self, data: list[list[str]]) -> None:
        with open(self.file, 'w', newline='', encoding='utf8') as file:
            w = csv.writer(file, delimiter=';')
            w.writerows(data)

    def read(self) -> list[list[str]]:
        with open(self.file, 'r', encoding='utf8') as file:
            data = [row for row in csv.reader(file, delimiter=';')]
            return data
        
    def delete(self, index: int) -> None | str:
        rows = self.read()
        try:
            rows.pop(index)
        except IndexError:
            return {'ERROR': 'Значение не найдено'}
        self.overwrite(rows)
