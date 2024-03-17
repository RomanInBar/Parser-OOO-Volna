from abstracts import AbstractServices, AbstractParser


class CommandsOfGUI:
    def __init__(self, services: AbstractServices, parser: AbstractParser) -> None:
        self.services = services
        self.parser = parser

    def get_all_data(self):
        return self.services.get_all_data()
    
    def add_value(self, *args):
        self.services.add_value(*args)

    def delete_value(self, *args):
        self.services.delete_value(*args)

    def init_start(self):
        self.parser.start()
    