import peewee as _PW

from .client import dbClient
from .schema import PermissionGroup_ENUM, TicketHolderType_ENUM



"""
This file populates the database with the data we need to let user's start 
using the application.

We also create an admin user here because only admins can create more admins.
"""



#region Data
# === Define data that will be seeded into the database ===

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

# === ===
#endregion



#region Seeding
# === Populate the database with seed data ===

# We use `Model.get_or_create()` so we don't get an error if the data already exists

# Films from the Film Catalogue
for filmTitle in FILM_TITLES:
  dbClient.tables.Film.get_or_create(
    title=filmTitle
  )

# Permission groups
for group in PermissionGroup_ENUM:
  dbClient.tables.PermissionGroup.get_or_create(
    id=group.value,
    readable=group.name
  )

# Ticket holder types
for type in TicketHolderType_ENUM:
  dbClient.tables.TicketHolderType.get_or_create(
    id=type.value,
    readable=type.name
  )

# Admin User
adminUser, _ = dbClient.tables.User.get_or_create(
  username=ADMIN_USER["username"],
  password=ADMIN_USER["password"]
)
adminPermission = dbClient.tables.PermissionGroup.get_by_id(PermissionGroup_ENUM.ADMIN.value)
dbClient.tables.UserPermissionGroups.get_or_create(
  user=adminUser,
  permissionGroup=adminPermission
)

# === ===
#endregion