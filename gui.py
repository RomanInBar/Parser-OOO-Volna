from tkinter import Entry, Label, Tk, ttk, Listbox, Variable
from typing import Callable

from abstracts import AbstractServices


class GraphicInterface(Tk):
    def __init__(self, services, *args, **kwargs) -> None:
        Tk.__init__(self, *args, **kwargs)
        self.title('Программа сбора информации о товарах')
        self.services: AbstractServices = services

        self.start = ttk.Button(self, text='Запуск', command=self.start, width=15)
        self.start.grid(column=0, row=0, rowspan=2)

        self.data = ttk.Button(self, text='Список значений', command=self.show_all_data, width=15)
        self.data.grid(column=1, row=0, rowspan=2)

    def redrawing(func: Callable):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            self = args[0]
            self.show_all_data()
            return response
        return wrapper

    def create_valid_values(self) -> list[str]:
        values = self.services.get_all_data()
        values = list(map(': '.join, values))
        return values

    @redrawing
    def add_value(self):
        old_value = self.old_value_field.get()
        new_value = self.new_value_field.get()
        data = [old_value, new_value]
        self.services.add_value(data)

    @redrawing
    def del_value(self):
        value = self.listbox.curselection()
        self.services.delete_value(value[0])

    def show_all_data(self) -> None:
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


    def start(self):
        ...
        
