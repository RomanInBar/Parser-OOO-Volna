from abc import ABC, abstractmethod
from typing import Iterable
from asyncio import AbstractEventLoop
from bs4 import BeautifulSoup


class AbstractStorage(ABC):
    @abstractmethod
    def write(self, path: str, data: list[str]) -> None: ...

    @abstractmethod
    def read(self, path: str) -> list[list[str]]: ...

    @abstractmethod
    def delete(self, path: str, index: int) -> None: ...


class AbstractParser(ABC):
    loop: AbstractEventLoop

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    async def scraping(self, url: str) -> str: ...


class AbstractDataProcessor(ABC):
    @abstractmethod
    def get_carts_of_products(self, page: BeautifulSoup) -> list[BeautifulSoup]: ...

    @abstractmethod
    def get_data_from_card(self, card: BeautifulSoup) -> list[str]: ...
