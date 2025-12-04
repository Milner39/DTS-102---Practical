import peewee as _PW

from client import DBClient


dbClient = DBClient()



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

  query = (User
    .select(User.id, User.username, User.contactPhone)
    .where(User.id == userId)
    .prefetch(UserPermissions, Permission, Booking)
  )
  user = next(iter(query), None)
  if user is None: return None

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


print(user__dataByAuth("admin", "123"))