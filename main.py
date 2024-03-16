from database import DatabaseCSV
from services import Services
from gui import GraphicInterface


PATH = 'Parser-OOO-Volna/database.csv'
db = DatabaseCSV(PATH)
services = Services(db)
app = GraphicInterface(services)
app.mainloop()
