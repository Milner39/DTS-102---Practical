# Database ORM
import peewee as _PW

def createClient():
  return _PW.SqliteDatabase("database/data.db", pragmas={ "foreign_keys": 1 })