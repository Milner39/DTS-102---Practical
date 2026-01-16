import peewee as _PW

from .client import dbClient as _dbClient



"""
This script defines the database module that encapsulates the database queries.

This ensures we don't accidentally call any subroutines that aren't protected 
by authentication or otherwise.
"""



class Database:
  """
  Class for interacting with the database from outside the `database` 
  module.
  """

  @staticmethod
  def user__idByAuth(username: str, password: str):
    """
    Return the user id of the entry in the User table that has the given 
    username and password.
    """

    User = _dbClient.tables.User

    try:
      user = User.get(
        (User.username == username) &
        (User.password == password)
      )
      return user.id
    except _PW.DoesNotExist:
      return None


  @staticmethod
  def user__dataByAuth(username: str, password: str):
    User = _dbClient.tables.User
    UserPermissionGroups = _dbClient.tables.UserPermissionGroups
    PermissionGroup = _dbClient.tables.PermissionGroup
    Booking = _dbClient.tables.Booking

    userId = __class__.user__idByAuth(username, password)
    if userId == None: return None

    res = (User
      .select(User.id, User.username, User.contactPhone)
      .where(User.id == userId)
      .prefetch(UserPermissionGroups, PermissionGroup, Booking)
    )
    if len(res) != 1: raise Exception()
    user = res[0]

    permissionGroups = [
      upg.permissionGroup.readable
      for upg in user.permissionGroups
    ]
    bookings = [
      { "film": b.film_id, "datetime": b.datetime }
      for b in user.bookings
    ]

    return {
      "username": user.username,
      "contactPhone": user.contactPhone,
      "permissionGroups": permissionGroups,
      "bookings": bookings,
    }