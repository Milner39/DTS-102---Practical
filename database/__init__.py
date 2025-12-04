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

  userId = user__idByAuth(username, password)
  if userId == None:
    return None
  
  query = (User
    .select(User.username, User.contactPhone)
    .where(User.id == userId)
  )
  return list(query.dicts())


print(user__dataByAuth("admin", "123"))