import peewee as _PW
from datetime import datetime as _DT

from .client import dbClient as _dbClient
from .queries import Queries as _dbQueries



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

  #region User

  @staticmethod
  def user__dataById(id: str):
    """
    Get the user's data given the entry's id.
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
      "id": user.id,
      "username": user.username,
      "contactPhone": user.contactPhone,
      "permissionGroups": permissionGroups,
      "bookings": bookings,
    }

  @staticmethod
  def user__idByAuth(username: str, password: str):
    """
    Return the id of the entry in the User table with the given username and 
    password.
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
    Get the user's data given their username and password.
    """

    userId = __class__.user__idByAuth(username, password)
    if userId is None: return None

    return __class__.user__dataById(userId)

  @staticmethod
  def user__register(username: str, password: str):
    """
    Register a new user.
    """

    user = _dbQueries.Tables.User.create(username, password)
    if user is None: return None

    assert user.id is str
    return __class__.user__dataById(user.id)

  #endregion


  #region Booking

  @staticmethod
  @_dbClient.database.atomic()
  def booking__create(userId: str, datetime: _DT, filmTitle: str, tickets):
    """
    Create a booking and tickets.
    """

    film = _dbQueries.Tables.Film.get_by_title(filmTitle)
    if film is None: return None

    booking = _dbQueries.Tables.Booking.create(userId, str(film.title), datetime)
    if booking is None: return None

    for ticket in tickets:
      _dbQueries.Tables.Ticket.create(str(booking.id), ticket)

  #endregion


  #region Film

  @staticmethod
  def film__allTitles():
    """
    Get every film title.
    """

    return [ film.title for film in _dbClient.Tables.Film.select() ]
  
  @staticmethod
  def film__idByTitle(title: str):
    """
    Return the id of the entry in the Film table with the given title.
    """

    film = _dbQueries.Tables.Film.get_by_title(title)
    if film is None: return None

    return film.title
    # The id of a film is the title but it shouldn't really be, so this is for
    # future fixes

  #endregion


  #region TicketHolderType

  @staticmethod
  def ticketHolderType__allTypes():
    """
    Get every ticket holder type.
    """

    return [ tType.readable for tType in _dbClient.Tables.TicketHolderType.select() ]

  #endregion