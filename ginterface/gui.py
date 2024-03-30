from tkinter import Tk, Label, Entry, ttk, Listbox, Variable, messagebox, NSEW
from typing import Callable
from functools import wraps
import logging
from utils.constants import FINAL_FILE, PATH_TO_URLS, PATH_TO_STORAGE
from utils.abstractions import AbstractParser, AbstractStorage
from utils.exceptions import ValuesNotFound, RepeatError
from threading import Thread


class GInterface(Tk):
    def __init__(self, parser: AbstractParser, storage: AbstractStorage, queue: list, *args, **kwargs) -> None:
        Tk.__init__(self, *args, **kwargs)
        self.parser = parser
        self.storage = storage
        self.queue = queue

    def mainloop(self, n: int = 0) -> None:
        self.title('Парсинг страниц сайта "Мир дерева"')
        self.width = 25
        self.draw_start_window()
        return super().mainloop(n)
    
    def draw_start_window(self):
        """Старторое окно программы."""
        self.start_button = ttk.Button(self, text='Запуск', command=self.start, width=self.width)
        self.start_button.grid(column=0, row=0)

        self.replaced_values_button = ttk.Button(self, text='Список значений', command=self.draw_window_with_list_values, width=self.width)
        self.replaced_values_button.grid(column=1, row=0)

        self.urlslist_button = ttk.Button(self, text='Список адресов', command=self.draw_urls_window, width=self.width)
        self.urlslist_button.grid(column=2, row=0)

        self.add_value_button = ttk.Button(self, text='Добавить', command=self.add_value, width=self.width)
        self.add_value_button.grid(column=0, row=1)

        self.del_value_button = ttk.Button(self, text='Удалить', command=self.del_value, width=self.width)
        self.del_value_button.grid(column=2, row=1)

        self.done = Label(self, text='')
        self.done.grid(column=0, row=2, columnspan=3, rowspan=2)
    
    def add_value(self):
        """Команда кнопки 'Добавить', инициализирует запись данных."""
        logging.info('Сработала кнопка "Добавить"')
        try:
            redrawing, path, value = self.check_add_value()
            self.storage.write(path, value)
            redrawing()
        except ValuesNotFound:
            msg = 'Вы забыли вписать данные для записи!'
            messagebox.showwarning('Предупреждение', msg)
        except RepeatError:
            msg = 'Такие данные уже записаны!'
            messagebox.showwarning('Предупреждение', msg)

    def check_del_value(self):
        """
        Проверяет, была ли выделена запись в списках.
        Возвращает три знаяения:
        func: Callable - функию перерисовки окна с новыми значениями
        path: str - путь к файлу
        value: tuple(int,) - данные для удаления.
        """
        if hasattr(self, 'valuesbox') and self.valuesbox.curselection():
            func = self.draw_window_with_list_values
            value = self.valuesbox.curselection()
            path = PATH_TO_STORAGE
        elif hasattr(self, 'urlbox') and self.urlsbox.curselection():
            func = self.draw_urls_window
            value = self.urlsbox.curselection()
            path = PATH_TO_URLS
        else:
            raise ValuesNotFound
        return func, path, value
    
    def check_add_value(self) -> tuple:
        """
        Проверяет, есть ли записи в окнах для ввода текста.
        Возвращает три знаяения:
        func: Callable - функию перерисовки окна с новыми значениями
        path: str - путь к файлу
        value: [] - данные для добавления.
        """
        if hasattr(self, 'input_url') and self.input_url.get():
            func = self.draw_urls_window
            path = PATH_TO_URLS
            value = [self.input_url.get().strip()]
        elif hasattr(self, 'old_value_field') and (self.old_value_field.get() and self.new_value_field.get()):
            func = self.draw_window_with_list_values
            old_value = self.old_value_field.get().strip()
            new_value = self.new_value_field.get().strip()
            path = PATH_TO_STORAGE
            value = [old_value, new_value]
        else:
            raise ValuesNotFound
        return func, path, value

    def del_value(self):
        """Команда кнопки 'Удалить', инициализирует удаление данных."""
        logging.info('Сработала кнопка "Удалить"')
        try:
            redrawing, path, value = self.check_del_value()
            self.storage.delete(path, value[0])
            redrawing()
        except (IndexError, ValuesNotFound):
            logging.exception(f'Запись для удаления не надйена.')
            msg = 'Запись на удаление не найдена!'
            messagebox.showerror('Удаление', msg)

    def draw_window_with_list_values(self) -> None:
        """Отрисока графического интерфейса."""
        self.old_value_label = Label(self, text='Текущее значение')
        self.old_value_label.grid(column=7, row=0, columnspan=2)
        self.old_value_field = Entry(self, width=30)
        self.old_value_field.grid(column=7, row=1, columnspan=2, sticky=NSEW)

        self.new_value_label = Label(self, text='Новое значение')
        self.new_value_label.grid(column=9, row=0, columnspan=2)
        self.new_value_field = Entry(self, width=30)
        self.new_value_field.grid(column=9, row=1, columnspan=2, sticky=NSEW)

        values = self.storage.read(PATH_TO_STORAGE)
        var = Variable(value=values)

        self.valuesbox = Listbox(listvariable=var)
        self.valuesbox.grid(column=7, row=2, columnspan=4, rowspan=9, sticky=NSEW)
        logging.info('Графический интерфейс отрисован')

    def start(self):
        """Команда кнопки 'Запуск', инициализирует запуск парсера."""
        logging.info('Сработала кнопка "Запуск"')
        self.start_button['text'] = 'Ждите'
        self.done['text'] = ''
        thread = Thread(target=self.parser.start, daemon=True)
        self.queue.append(self.end)
        thread.start()

    def end(self):
        self.start_button['text'] = 'Запуск'
        self.done['text'] = f'Готово\nФайл сохранен на рабочем столе\nпод именем {FINAL_FILE}'

    def draw_urls_window(self):
        values = self.storage.read(PATH_TO_URLS)
        var = Variable(value=values)

        self.text_url = Label(self, text='Введите адрес:')
        self.text_url.grid(column=0, row=4, columnspan=3, sticky='w')
        self.input_url = Entry(self)
        self.input_url.grid(column=0, row=5, columnspan=3, sticky='nsew')

        self.list_urls_text = Label(text='Список адресов')
        self.list_urls_text.grid(column=0, row=6, columnspan=3, sticky='w')
        self.urlsbox = Listbox(listvariable=var)
        self.urlsbox.grid(column=0, row=7, columnspan=7, rowspan=6, sticky='nsew')
