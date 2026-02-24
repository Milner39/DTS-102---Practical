import peewee as _PW

from .models import dbProxy as _dbProxy, Models as _Models



#region Utils

class Utils:

  @staticmethod
  def initializeProxy(database: _PW.Database):
    """
    "Swaps in" the real database object to the proxy.

    This must be done before creating the tables.
    """
    _dbProxy.initialize(database)


  @staticmethod
  def createTables(database: _PW.Database):
    """
    Initialise the database proxy and create all tables defined in the schema.

    Returns all the tables.
    """

    __class__.initializeProxy(database)

    database.create_tables(_Models.all)

    return _Models

#endregion
