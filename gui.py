from tkinter import Entry, Label, Tk, ttk


class GUIOfParser(Tk):
    def __init__(self, *args, **kwargs) -> None:
        Tk.__init__(self, *args, **kwargs)
        self.title('Программа сбора информации о товарах')
        
        self.old_value_label = Label(self, text='Текущее значение')
        self.old_value_label.grid(column=0, row=0)
        self.old_value_field = Entry(self, width=40)
        self.old_value_field.grid(column=0, row=1)

        self.new_value_label = Label(self, text='Новое значение')
        self.new_value_label.grid(column=1, row=0)
        self.new_value_field = Entry(self, width=40)
        self.new_value_field.grid(column=1, row=1)

        self.add_value_button = ttk.Button(self, text='Добавить', command=...)
        self.add_value_button.grid(column=0, row=4, columnspan=2, rowspan=2)

        self.start_button = ttk.Button(self, text='Запуск', command=...)
        self.start_button.grid(column=0, row=6, rowspan=2)

        self.list_of_values = ttk.Button(self, text='Список заменяемых слов', command=...)
        self.list_of_values.grid(column=1, row=6, rowspan=2)


app = GUIOfParser()
app.mainloop()
