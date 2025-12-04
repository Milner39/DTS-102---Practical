import peewee as _PW
import sqlite3 as _SQLITE3

from client import DBClient
from schema import ENUM__Permission_level, ENUM__Ticket_holderType

dbClient = DBClient()


FILM_TITLES = [
  "Jurassic Cabin",
  "The Dark Night",
  "The Nightmare on First Street",
  "Quantum Mania",
  "The Game of Thorns",
  "The Shape of Time"
]



# === Populate the database with data we know we'll need ===
# We use `Model.get_or_create()` so we don't get an error if the data already exists

# Admin User
adminUser = dbClient.tables.User.get_or_create(
  username="admin",
  password="123"
)
adminPermission = dbClient.tables.Permission.get_or_create(
  level=ENUM__Permission_level.ADMIN
)
dbClient.tables.UserPermissions.get_or_create(
  user=adminUser,
  permission=adminPermission
)

# Films from the Film Catalogue
for filmTitle in FILM_TITLES:
  dbClient.tables.Film.get_or_create(
    title=filmTitle
  )

# === Populate the database with data we know we'll need ===