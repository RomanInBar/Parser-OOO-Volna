from abc import abstractmethod, ABC
from tkinter import Tk


class AbstractDatabseCSV(ABC):
    @abstractmethod
    def write(self, value: list[str]) -> None:
        ...

    @abstractmethod
    def read(self) -> list[list[str]]:
        ...

    @abstractmethod
    def delete(self, value: list[str]) -> None:
        ...


class ABSGraphicInterface(ABC):    
    old_value_label: Tk
    old_value_field: Tk
    new_value_label: Tk
    new_value_field: Tk
    add_value_button: Tk
    start_button: Tk
    list_of_values: Tk


class AbstractServices(ABC):
    @abstractmethod
    def add_value(self, value: list[str]):
        ...

    @abstractmethod
    def get_all_data(self) -> list[list[str]]:
        ...

    @abstractmethod
    def delete_value(self, index: str):
        ...

    @abstractmethod
    def start(self):
        ...



