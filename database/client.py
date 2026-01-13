import os
import peewee as _PW

from .schema import createTables



"""
This file provides utilities for creating the database and database client.

We also create an admin user here because only admins can create more admins.
"""



def createDatabase():
  """Create/Get the database"""

  dbPath = os.path.join(os.path.dirname(__file__), "./data.db")
  return _PW.SqliteDatabase(dbPath, pragmas={ "foreign_keys": 1 })



class DBClient:
  """Class for interacting with the database"""

  def __init__(self):
    self.database = createDatabase()
    self.database.connect()

    self.tables = createTables(self.database)



dbClient = DBClient()
"""The database client we use to interact with the database"""