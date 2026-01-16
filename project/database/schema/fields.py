import peewee as _PW
import uuid as _UUID



#region Fields

class Fields:
  """A class containing all of the custom `Field` objects"""

  # === Define a base class to extend when creating Fields ===

  class BaseField:
    """
    A base Fields to extend when creating custom Fields for the Models.

    This lets us give all the Fields some common attributes.
    """

    @staticmethod
    def create() -> _PW.Field:
      return _PW.Field()

  # === ===


  class PkUUID(BaseField):
    """Primary Key that generates a random UUID on creation"""

    @staticmethod
    def create():
      return _PW.UUIDField(
        primary_key=True,
        default=_UUID.uuid4,
        unique=True,
        null=False,
      )

#endregion