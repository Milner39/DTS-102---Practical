import os
import peewee as _PW
from schema import createTables



def createDatabase():
  dbPath = os.path.join(os.path.dirname(__file__), "./data.db")
  return _PW.SqliteDatabase(dbPath, pragmas={ "foreign_keys": 1 })


class DBClient:
  def __init__(self):
    self.database = createDatabase()
    self.database.connect()

    self.tables = createTables(self.database)