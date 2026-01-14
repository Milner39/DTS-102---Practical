from .queries import Queries as dbQueries

from .client import dbClient
from .schema import PermissionGroup_ENUM, TicketHolderType_ENUM



"""
This file populates the database with the data we need to let users start 
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


# Films from the Film Catalogue
for filmTitle in FILM_TITLES:
  dbClient.tables.Film.get_or_create(
    title=filmTitle
  )

# Permission groups
for group in PermissionGroup_ENUM:
  dbQueries.Tables.PermissionGroup.update_or_create(
    id=group.value,
    readable=group.name
  )

# Ticket holder types
for type in TicketHolderType_ENUM:
  dbQueries.Tables.TicketHolderType.update_or_create(
    id=type.value,
    readable=type.name
  )

# Admin User
dbQueries.Tables.User.delete_then_create_admin(
  username=ADMIN_USER["username"],
  password=ADMIN_USER["password"]
)

# === ===
#endregion