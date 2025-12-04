import peewee as _PW

from client import DBClient
from schema import PermissionLevels, TicketHolderTypes

dbClient = DBClient()


ADMIN_USER = {
  "username": "admin",
  "password": "123"
}

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

# Films from the Film Catalogue
for filmTitle in FILM_TITLES:
  dbClient.tables.Film.get_or_create(
    title=filmTitle
  )

# Permission levels
for level in PermissionLevels:
  dbClient.tables.Permission.get_or_create(
    id=level.value,
    readable=level.name
  )

# Ticket holder types
for type in TicketHolderTypes:
  dbClient.tables.TicketHolderType.get_or_create(
    id=type.value,
    readable=type.name
  )

# Admin User
adminUser, _ = dbClient.tables.User.get_or_create(
  username=ADMIN_USER["username"],
  password=ADMIN_USER["password"]
)
adminPermission = dbClient.tables.Permission.get_by_id(PermissionLevels.ADMIN.value)
dbClient.tables.UserPermissions.get_or_create(
  user=adminUser,
  permission=adminPermission
)

# === Populate the database with data we know we'll need ===