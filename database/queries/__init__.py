import peewee as _PW

from ..client import dbClient
from ..schema import Schema



"""
This script defines the database queries we use in the rest of the codebase
"""



# Get concise references to common classes
Models  =  Schema.Models
ENUMs   =  Schema.ENUMs



#region Queries

class Queries:
  """A class containing all of the custom database queries"""

  class Tables:
    """Basic queries that typically only interact with a single table"""

    class _BaseQueries:
      """Common queries shared to all tables"""

      table = Models._BaseModel
      """
      Provides a reference to a Model that will be overridden depending on the 
      table query class that extends this one.
      """

      @staticmethod
      def delete_all() -> None:
        """Delete every entry in this table"""

        __class__.table.delete().execute()

      # @staticmethod
      # def update_or_create(**kwargs) -> type[table]:
      #   pass



    #region Film
    # === ===
    class Film(_BaseQueries):
      """Queries for the `Film` table"""

      table = dbClient.tables.Film

    # === ===
    #endregion PFilm


    #region Permission Group
    # === ===
    class PermissionGroup(_BaseQueries):
      """Queries for the `PermissionGroup` table"""

      table = dbClient.tables.PermissionGroup

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
          # Will raise if no entry found
          entry = __class__.table.get_by_id(id)

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

    # === ===
    #endregion Permission Group


    #region Ticket Holder Type
    # === ===
    class TicketHolderType(_BaseQueries):
      """Queries for the `TicketHolderType` table"""

      table = dbClient.tables.TicketHolderType

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
          # Will raise if no entry found
          entry = __class__.table.get_by_id(id)

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

    # === ===
    #endregion Ticket Holder Type


    #region User
    # === ===
    class User(_BaseQueries):
      """Queries for the `User` table"""

      table = dbClient.tables.User

      @staticmethod
      def id_by_username(username: str) -> (int | None):
        """
        Attempts to find an User entry by it's username
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
      def delete_then_create(username: str, password: str) -> Models.User:
        """
        Attempts to find an entry by it's username:
          - if found -> delete the entry

        Create the entry

        Returns the entry
        """

        userId = __class__.id_by_username(username=username)

        if (userId is not None):
          __class__.table.delete_by_id(userId)

        user = __class__.table.create(
          username=username,
          password=password
        )

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
        adminPG = dbClient.tables.PermissionGroup.get_by_id(
          pk=ENUMs.PermissionGroup_ENUM.ADMIN.value
        )

        # Give the admin user the admin permission group
        dbClient.tables.UserPermissionGroups.create(
          user=adminUser,
          permissionGroup=adminPG
        )

        return adminUser

    # === ===
    #endregion User

#endregion