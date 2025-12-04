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
  UserPermissions = dbClient.tables.UserPermissions
  Permission = dbClient.tables.Permission
  Booking = dbClient.tables.Booking

  userId = user__idByAuth(username, password)
  if userId == None: return None

  res = (User
    .select(User.id, User.username, User.contactPhone)
    .where(User.id == userId)
    .prefetch(UserPermissions, Permission, Booking)
  )
  if len(res) != 1: raise Exception()
  user = res[0]

  permissions = [
    up.permission.readable
    for up in user.permissions
  ]
  bookings = [
    { "film": b.film_id, "datetime": b.datetime }
    for b in user.bookings
  ]

  return {
    "username": user.username,
    "contactPhone": user.contactPhone,
    "permissions": permissions,
    "bookings": bookings,
  }