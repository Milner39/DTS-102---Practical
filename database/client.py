import os
import peewee as _PW
from schema import createTables



def createDatabase():
  dbPath = os.path.join(os.path.dirname(__file__), "./data.db")
  return _PW.SqliteDatabase(dbPath, pragmas={ "foreign_keys": 1 })


class DBClient:
  database = createDatabase()
  tables = createTables(database)

  def __init__(self):
    self.database.connect()