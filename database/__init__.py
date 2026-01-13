import peewee as _PW

from .client import DBClient


dbClient = DBClient()



# Return the user id of the entry in the User table that has the given username and password
def user__idByAuth(username: str, password: str):
  User = dbClient.tables.User

  try:
    user = User.get(
      (User.username == username) &
      (User.password == password)
    )
    return user.id
  except _PW.DoesNotExist:
    return None


def user__dataByAuth(username: str, password: str):
  User = dbClient.tables.User
  UserPermissionGroups = dbClient.tables.UserPermissionGroups
  PermissionGroup = dbClient.tables.PermissionGroup
  Booking = dbClient.tables.Booking

  userId = user__idByAuth(username, password)
  if userId == None: return None

  res = (User
    .select(User.id, User.username, User.contactPhone)
    .where(User.id == userId)
    .prefetch(UserPermissionGroups, PermissionGroup, Booking)
  )
  if len(res) != 1: raise Exception()
  user = res[0]

  permissionGroups = [
    up.permissionGroup.readable
    for up in user.permissionGroups
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