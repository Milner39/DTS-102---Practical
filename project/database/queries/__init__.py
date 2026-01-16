import peewee as _PW
from datetime import datetime as _DT

from ..client import dbClient
from ..schema import Schema



"""
This script defines the database queries we use in the rest of the codebase
"""



# Get concise references to common classes
Models  =  Schema.Models
ENUMs   =  Schema.ENUMs



#region Queries

# === Define a class to extend when creating the queries for db tables ===

class _BaseQueries:
  """Common queries shared to all tables"""

  table = Models._BaseModel
  """
  Provides a reference to a Model that will be overridden depending on the 
  table query class that extends this one.
  """

  @classmethod
  def delete_all(cls) -> None:
    """Delete every entry in this table"""

    cls.table.delete().execute()

  @classmethod
  def get_by_id(cls, id):
    """
    Attempts to find an entry by it's id
      - if found -> return the entry
      - else -> return `None`
    """

    try:
      return cls.table.get_by_id(id)
    except _PW.DoesNotExist:
      return None

  # @staticmethod
  # def update_or_create(**kwargs) -> type[table]:
  #   pass

# === ===


#region Booking

class Booking(_BaseQueries):
  """Queries for the `Booking` table"""

  table = dbClient.Tables.Booking

  @staticmethod
  @dbClient.database.atomic()
  def create(userId: str, filmId: str, datetime: _DT) -> Models.Booking | None:
    """
    Create a new booking

    Return the entry
    """

    user: Models.User | None = User.get_by_id(userId)
    film: Models.Film | None = Film.get_by_id(filmId)

    if (
      user is None or
      film is None
    ): return None

    booking = __class__.table.create(
      user=user,
      film=film,
      datetime=datetime
    )

    return booking

#endregion


#region Film

class Film(_BaseQueries):
  """Queries for the `Film` table"""

  table = dbClient.Tables.Film

  @staticmethod
  def get_by_title(title: str) -> Models.Film | None:
    """
    Attempts to find an entry by it's title
      - if found -> return the entry
      - else -> return `None`
    """

    try:
      return dbClient.Tables.Film.get(
        (__class__.table.title == title)
      )
    except _PW.DoesNotExist:
      return None

#endregion


#region PermissionGroup

class PermissionGroup(_BaseQueries):
  """Queries for the `PermissionGroup` table"""

  table = dbClient.Tables.PermissionGroup

  @staticmethod
  @dbClient.database.atomic()
  def update_or_create(id: int, readable: str) -> Models.PermissionGroup:
    """
    Attempts to find an entry by it's id:
      - if not found -> create the entry
      - if found -> update the entry

    Returns the entry
    """

    try:
      entry = __class__.get_by_id(id)
      if entry is None: raise _PW.DoesNotExist

      __class__.table.update(
        id=id,
        readable=readable
      )

    except _PW.DoesNotExist:
      entry = __class__.table.create(
        id=id,
        readable=readable
      )

    return entry

#endregion


#region Ticket

class Ticket(_BaseQueries):
  """Queries for the `Ticket` table"""

  table = dbClient.Tables.Ticket


  @staticmethod
  @dbClient.database.atomic()
  def create(bookingId: str, type: str) -> Models.Ticket | None:
    """
    Create a new ticket

    Return the entry
    """

    booking: Models.Booking | None = Booking.get_by_id(bookingId)
    ticketType: Models.TicketHolderType | None = TicketHolderType.get_by_readable(type)

    if (
      booking is None or
      ticketType is None
    ): return None

    ticket = __class__.table.create(
      booking=booking,
      holderType=ticketType,
      paidPriceGBP=5.00
    )

    return ticket

#endregion


#region TicketHolderType

class TicketHolderType(_BaseQueries):
  """Queries for the `TicketHolderType` table"""

  table = dbClient.Tables.TicketHolderType

  @staticmethod
  def get_by_readable(readable: str):
    """
    Attempts to find an entry by it's id
      - if found -> return the entry
      - else -> return `None`
    """

    try:
      return __class__.table.get(
        (__class__.table.readable == readable)
      )
    except _PW.DoesNotExist:
      return None


  @staticmethod
  @dbClient.database.atomic()
  def update_or_create(id: int, readable: str) -> Models.TicketHolderType:
    """
    Attempts to find an entry by it's id:
      - if not found -> create the entry
      - if found -> update the entry

    Returns the entry
    """

    try:
      entry = __class__.table.get_by_id(id)
      if entry is None: raise _PW.DoesNotExist

      __class__.table.update(
        id=id,
        readable=readable
      )

    except _PW.DoesNotExist:
      entry = __class__.table.create(
        id=id,
        readable=readable
      )

    return entry

#endregion


#region User

class User(_BaseQueries):
  """Queries for the `User` table"""

  table = dbClient.Tables.User

  @staticmethod
  def id_by_username(username: str) -> (int | None):
    """
    Attempts to find a User entry by it's username
      - if found -> return it's id
      - if not found -> return `None`
    """

    try:
      entry = __class__.table.get(
        (__class__.table.username == username)
      )
      return entry.id

    except _PW.DoesNotExist:
      return None


  @staticmethod
  @dbClient.database.atomic()
  def create(username: str, password: str) -> Models.User | None:
    """
    Attempts to find an entry by it's username:
      - if found -> return `None`

    Create the entry

    Return the entry
    """

    userId = __class__.id_by_username(username=username)

    if (userId is not None):  # username taken
      return None

    user = __class__.table.create(
      username=username,
      password=password
    )

    return user


  @staticmethod
  @dbClient.database.atomic()
  def delete_then_create(username: str, password: str) -> Models.User:
    """
    Attempts to find an entry by it's username:
      - if found -> delete the entry

    Create the entry

    Return the entry
    """

    userId = __class__.id_by_username(username=username)

    if (userId is not None):
      __class__.table.delete_by_id(userId)

    user = __class__.create(
      username=username,
      password=password
    )
    assert user is not None

    return user


  @staticmethod
  @dbClient.database.atomic()
  def delete_then_create_admin(username: str, password: str) -> Models.User:
    """
    Creates a User entry and gives them the `ADMIN` PermissionGroup
    """

    # Crate the admin
    adminUser = __class__.delete_then_create(
      username=username,
      password=password
    )

    # Get the admin permission group
    adminPG = PermissionGroup.get_by_id(
      ENUMs.PermissionGroup_ENUM.ADMIN.value
    )

    # Give the admin user the admin permission group
    dbClient.Tables.UserPermissionGroups.create(
      user=adminUser,
      permissionGroup=adminPG
    )

    return adminUser

#endregion


#region UserPermissionGroups

class UserPermissionGroups(_BaseQueries):
  """Queries for the `UserPermissionGroups` table"""

  table = dbClient.Tables.UserPermissionGroups

#endregion


class Queries:
  """A class containing all of the custom database queries"""

  class Tables:
    """Basic queries that typically only interact with a single table"""

    Booking               =  Booking
    Film                  =  Film
    PermissionGroup       =  PermissionGroup
    Ticket                =  Ticket
    TicketHolderType      =  TicketHolderType
    User                  =  User
    UserPermissionGroups  =  UserPermissionGroups

#endregion