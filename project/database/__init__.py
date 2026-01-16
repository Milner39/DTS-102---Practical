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
  def user__dataById(id: str):
    """
    Get the user's data given the entry's id
    """

    Tables = _dbClient.Tables
    User = Tables.User
    UserPermissionGroups = Tables.UserPermissionGroups
    PermissionGroup = Tables.PermissionGroup
    Booking = Tables.Booking

    res = (User
      .select(User.id, User.username, User.contactPhone)
      .where(User.id == id)
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


  @staticmethod
  def user__idByAuth(username: str, password: str):
    """
    Return the user id of the entry in the User table that has the given 
    username and password.
    """

    User = _dbClient.Tables.User

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
    """
    Get the user's data given their username and password
    """

    userId = __class__.user__idByAuth(username, password)
    if userId == None: return None

    return __class__.user__dataById(userId)


  @staticmethod
  def user__register(username: str, password: str):
    pass