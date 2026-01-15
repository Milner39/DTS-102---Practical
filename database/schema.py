import enum as _ENUM
import uuid as _UUID
import typing as _TYPING

import peewee as _PW



"""
This file defines the schema for our tables, and the relationships between them.

A schema tell our database client what tables should exist in our database, and 
the datatypes of the fields in the tables.

The schema is made up from `Model` objects, each defines the structure of a 
table in the database.

When defining the tables, we can add constraints on each field like 
`primary_key` for primary keys, `unique` to enforce unique values, and `null` 
to prevent `None` values.

We also can do more complicated things like composite keys and indexes.
"""



class Schema:
  """The Schema module"""

  """
  We define this database proxy (fake database object) so the base table model 
  has a reference to the database. We "swap in" the real database later.

  This is just a requirement when using `peewee`, I don't fully understand it, 
  but if you do, maybe you can improve this comment.
  """
  __dbProxy = _PW.DatabaseProxy()



  #region ENUMs

  class ENUMs:
    """A class containing all of the `ENUM` classes for populating tables"""

    # These are for tables where we know there are a finite amount of entries, 
    # and we know the entries before hand.

    class PermissionGroup_ENUM(_ENUM.Enum):
      """Enum for the `PermissionGroup` table"""
      ADMIN = 0
      DEVELOPER = 1

    class TicketHolderType_ENUM(_ENUM.Enum):
      """Enum for the `TicketHolderType` table"""
      ADULT = 0
      TEENAGER = 1
      CHILD = 2
      STUDENT = 3

  #endregion ENUMs



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

  #endregion Fields



  #region Models

  class Models:
    """A class containing all of the `Model` objects (tables)"""

    # === Define a base class to extend when creating Models ===

    class BaseModel(_PW.Model):
      """
      A base Model to extend when creating Models for the database schema.

      This lets us give all the Models some common attributes.
      """

      class Meta:
        # This tells each table class what database it's in
        database = Schema.__dbProxy
        legacy_table_names = False


    """
    `peewee` removes `Model.Meta` at runtime, keep a stand-in for type checkers 
    to ignore annoying syntax messages.
    """
    if _TYPING.TYPE_CHECKING:
      BaseMeta = BaseModel.Meta
    else:
      class BaseMeta:
        pass

    # === ===


    class User(BaseModel):
      """Users of this application"""

      id = Fields.PkUUID.create()
      """UUID primary key"""

      username = _PW.CharField(
        max_length=64,
        unique=True,
        null=False,
      )
      """A unique, non-null username used for registration / login"""

      password = _PW.CharField(
        max_length=64,
        null=False,
      )
      """
      Used to authenticate a user by their username
      
      Will be stored as plain-text because encryption is out of scope
      """

      contactPhone = _PW.CharField(
        max_length=32,
        null=True,
      )
      """
      An optional phone number (string) used to contact the user
      """


    class PermissionGroup(BaseModel):
      """Groups that determine what permissions a user has"""

      id = _PW.SmallIntegerField(
        primary_key=True,
        unique=True,
        null=False,
      )
      """The value of the member in `PermissionGroup_ENUM`"""

      readable = _PW.CharField(
        max_length=32,
        unique=True,
        null=False,
      )
      """The name of the member in `PermissionGroup_ENUM`"""


    class UserPermissionGroups(BaseModel):
      """Join table for `Users` and `PermissionGroup`"""

      user = _PW.ForeignKeyField(Models.User,
        backref="permissionGroups",
        on_update="CASCADE",
        on_delete="CASCADE",
      )
      """Entry in `User` table"""

      permissionGroup = _PW.ForeignKeyField(Models.PermissionGroup,
        backref="users",
        on_update="CASCADE",
        on_delete="CASCADE",
      )
      """Entry in `PermissionGroup` table"""

      class Meta(Models.BaseMeta):
        primary_key = _PW.CompositeKey("user", "permissionGroup")



    class Film(BaseModel):
      """All past and future films that have and will be shown"""

      title = _PW.CharField(
        primary_key=True,
        max_length=64,
        unique=True,
        null=False,
      )
      """The title of the film"""


    class Booking(BaseModel):
      """Bookings for films made by users"""

      id = Fields.PkUUID.create()
      """UUID primary key"""

      user = _PW.ForeignKeyField(User,
        backref="bookings",
        on_update="CASCADE"
        # Do not delete bookings if the user has been deleted
      )
      """Entry in `User` table"""

      film = _PW.ForeignKeyField(Film,
        backref="bookings",
        on_update="CASCADE",
        on_delete="CASCADE",
      )
      """Entry in `Film` table"""

      datetime = _PW.DateTimeField(
        null=False
      )
      """
      Date & time of the showing of the film

      We assume that all films are always showing so a user can make a booking for 
      any film at any time, because this is just a College assignment, and not the 
      real world :)
      """



    class TicketHolderType(BaseModel):
      """Ticket types that determine how much a ticket costs"""

      id = _PW.SmallIntegerField(
        primary_key=True,
        unique=True,
        null=False,
      )
      """The value of the member in `TicketHolderType_ENUM`"""

      readable = _PW.CharField(
        max_length=32,
        unique=True,
        null=False,
      )
      """The name of the member in `TicketHolderType_ENUM`"""



    class Ticket(BaseModel):
      """Tickets for bookings made by users"""

      id = Fields.PkUUID.create()
      """UUID primary key"""

      booking = _PW.ForeignKeyField(Model.Booking,
        backref="tickets",
        on_update="CASCADE",
        on_delete="CASCADE",
      )
      """Entry in `Booking` table"""

      holderName = _PW.CharField(
        max_length=64
      )
      """Optional ticket holder name"""

      holderType = _PW.ForeignKeyField(Model.TicketHolderType,
        backref="tickets",
      )
      """Entry in `TicketHolderType` table"""

      paidPriceGBP = _PW.DecimalField(
        max_digits=5,
        decimal_places=2,
        auto_round=True,
        null=False
      )
      """
      The calculated amount the user paid for the ticket at the point of booking.

      This *would* let us refund the correct amount to the user in case of a 
      cancellation, and makes sure the refunded amount isn't too little / much 
      because of potential price changes / deals.
      """

  #endregion Models



  #region Utils

  class Utils:

    @staticmethod
    def initializeProxy(database: _PW.Database):
      """
      "Swaps in" the real database object to the proxy.

      This must be done before creating the tables.
      """
      _dbProxy.initialize(database)


    @staticmethod
    def createTables(database: _PW.Database):
      """
      Initialise the database proxy and create all tables defined in the schema.

      Returns all the tables.
      """

      __class__.initializeProxy(database)

      database.create_tables([
        Models.User,
        Models.UserPermissionGroups,
        Models.PermissionGroup,
        Models.Film,
        Models.Booking,
        Models.Ticket,
        Models.TicketHolderType
      ])

      return Models

  #endregion Utils