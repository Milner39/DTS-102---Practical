import peewee as _PW

from ..client import dbClient
from ..schema import Tables
from ..exceptions import QueryExceptions



def delete_all():
  dbClient.tables.PermissionGroup.delete().execute()


def update_or_create(id: int, readable: str) -> Tables.PermissionGroup:
  try:
    # Will raise if no entry found
    entry = dbClient.tables.PermissionGroup.get_by_id(id)

    dbClient.tables.PermissionGroup.update(
      id=id,
      readable=readable
    )

  except _PW.DoesNotExist:
    entry = dbClient.tables.PermissionGroup.create(
      id=id,
      readable=readable
    )

  return entry