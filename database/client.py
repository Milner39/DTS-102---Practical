import os
import peewee as _PW


def createClient():
  dbPath = os.path.join(os.path.dirname(__file__), "./data.db")
  return _PW.SqliteDatabase(dbPath, pragmas={ "foreign_keys": 1 })