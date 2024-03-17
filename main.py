from database import DatabaseCSV
from services import Services
from gui_commands import CommandsOfGUI
from gui import GraphicInterface
from parserv import StartParser
from constants import PATH_TO_DB, PATH_TO_URLS, PATH_TO_FILE


class InitialisationProgramm:
    def __init__(self) -> None:
        pass

    def get_urls(self, path: str) -> list[str]:
        with open(path, 'r', encoding='utf8') as file:
            urls = [row.strip() for row in file]
            return urls

    def get_names(self, db: DatabaseCSV) -> dict[str, str]:
        data = {old: new for [old, new] in db.read()}
        return data
            
    def init_db(self, path: str) -> DatabaseCSV:
        db = DatabaseCSV(path)
        return db

    def init_services(self, db: DatabaseCSV) -> Services:
        services = Services(db)
        return services

    def init_parser(self, urls: list[str], change_names: dict[str, str], path_save_file: str) -> StartParser:
        parser = StartParser(urls, change_names, path_save_file)
        return parser

    def init_commangs(self, services: Services, parser: StartParser) -> CommandsOfGUI:
        gui_commands = CommandsOfGUI(services, parser)
        return gui_commands

    def init_app(self, commands: CommandsOfGUI) -> GraphicInterface:
        app = GraphicInterface(commands)
        return app


def main():
    init = InitialisationProgramm()
    db = init.init_db(PATH_TO_DB)
    servis = init.init_services(db)
    urls = init.get_urls(PATH_TO_URLS)
    names = init.get_names(db)
    parser = init.init_parser(urls, names, PATH_TO_FILE) 
    gui_commands = init.init_commangs(servis, parser)
    app = init.init_app(gui_commands)
    app.mainloop()


if __name__ == '__main__':
    main()
