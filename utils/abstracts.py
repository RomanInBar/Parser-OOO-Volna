from abc import abstractmethod, ABC


class AbstractDatabseCSV(ABC):
    """Абстрактный класс хранилища данных."""
    @abstractmethod
    def write(self, value: list[str]) -> None:
        ...

    @abstractmethod
    def read(self) -> list[list[str]]:
        ...

    @abstractmethod
    def delete(self, value: list[str]) -> None:
        ...


class AbstractServices(ABC):
    """Абстрактный класс сервисов графического интерфейса."""
    @abstractmethod
    def add_value(self, value: list[str]):
        ...

    @abstractmethod
    def get_all_data(self) -> list[list[str]]:
        ...

    @abstractmethod
    def delete_value(self, index: str):
        ...


class AbstractParser(ABC):
    """Абстрактный класс парсера."""
    @abstractmethod
    def start(self):
        ...


class AbstractGUICommands(ABC):
    @abstractmethod
    def get_all_data(self):
        ...

    @abstractmethod
    def add_value(self, *args):
        ...

    @abstractmethod
    def delete_value(self, *args):
        ...

    @abstractmethod
    def init_start(self):
        ...
