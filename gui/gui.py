from tkinter import Entry, Label, Tk, ttk, Listbox, Variable
from typing import Callable
from utils.abstracts import AbstractGUICommands
import logging
from utils.constants import RESULT_FILE_NAME
from functools import wraps


class GraphicInterface(Tk):
    """Графический интерфейс."""
    def __init__(self, services, *args, **kwargs) -> None:
        Tk.__init__(self, *args, **kwargs)
        self.title('Программа сбора информации о товарах')
        self.services: AbstractGUICommands = services
    
    def mainloop(self, n: int = 0) -> None:
        self.draw_start_window()
        return super().mainloop(n)
        
    def draw_start_window(self):
        """Старторое окно программы."""
        self.start_button = ttk.Button(self, text='Запуск', command=self.start, width=15)
        self.start_button.grid(column=0, row=0, rowspan=2)

        self.replaced_values_button = ttk.Button(self, text='Список значений', command=self.draw_window_with_list_values, width=15)
        self.replaced_values_button.grid(column=1, row=0, rowspan=2)

        self.done = Label(self, text='')
        self.done.grid(column=0, row=2, columnspan=2)

    def redrawing(func: Callable):
        """Декоратор для перерисовки окна со списком значений."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            self = args[0]
            self.draw_window_with_list_values()
            logging.info('Графический интерфейс перерисован')
            return response
        return wrapper

    def create_valid_values(self) -> list[str]:
        """Переработка данных в валидную вариацию."""
        values = self.services.get_all_data()
        values = list(map(': '.join, values))
        logging.info('Данные приведены к нужному виду')
        return values

    @redrawing
    def add_value(self):
        """Команда кнопки 'Добавить', инициализирует добавление данных."""
        logging.info('Сработала кнопка "Добавить"')
        old_value = self.old_value_field.get()
        new_value = self.new_value_field.get()
        data = [old_value, new_value]
        self.services.add_value(data)

    @redrawing
    def del_value(self):
        """Команда кнопки 'Удалить', инициализирует удаление данных."""
        logging.info('Сработала кнопка "Удалить"')
        value = self.listbox.curselection()
        try:
            self.services.delete_value(value[0])
        except IndexError:
            logging.exception('Индекс записи из списка не найден в хранилище данных.')

    def draw_window_with_list_values(self) -> None:
        """Отрисока графического интерфейса."""
        self.old_value_label = Label(self, text='Текущее значение')
        self.old_value_label.grid(column=3, row=0)
        self.old_value_field = Entry(self, width=30)
        self.old_value_field.grid(column=3, row=1)

        self.new_value_label = Label(self, text='Новое значение')
        self.new_value_label.grid(column=4, row=0)
        self.new_value_field = Entry(self, width=30)
        self.new_value_field.grid(column=4, row=1)

        self.add_value_button = ttk.Button(self, text='Добавить', command=self.add_value, width=10)
        self.add_value_button.grid(column=5, row=1)

        self.del_value_button = ttk.Button(self, text='Удалить', command=self.del_value, width=10)
        self.del_value_button.grid(column=6, row=1)

        values = self.create_valid_values()
        var = Variable(value=values)

        self.listbox = Listbox(listvariable=var, width=61)
        self.listbox.grid(column=3, row=2, columnspan=2)
        logging.info('Графический интерфейс отрисован')

    def start(self):
        """Команда кнопки 'Запуск', инициализирует запуск парсера."""
        logging.info('Сработала кнопка "Запуск"')
        self.services.init_start()
        self.done['text'] = f'Готово\nФайл сохранен на рабочем столе\nпод именем {RESULT_FILE_NAME}'
