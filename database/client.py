import os as _OS
import peewee as _PW

from .schema.utils import Utils as _SchemaUtils



"""
This script provides utilities for creating the database and database client.

We also create an admin user here because only admins can create more admins.
"""



class DBClient:
  """Class for interacting with the database"""

  @staticmethod
  def createDatabase():
    """Create/Get the database"""

    dbPath = _OS.path.join(_OS.path.dirname(__file__), "./data.db")
    return _PW.SqliteDatabase(dbPath, pragmas={ "foreign_keys": 1 })


  def __init__(self):
    """Initialise a client for the database"""

    self.database = __class__.createDatabase()
    self.database.connect()

    self.tables = _SchemaUtils.createTables(self.database)



dbClient = DBClient()
"""The instance of the database client we use to interact with the database"""