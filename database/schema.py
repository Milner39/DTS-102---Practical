import enum as _ENUM
import uuid as _UUID
import typing as _TYPING

import peewee as _PW



"""
This file defines the schema for our tables, and the relationships between them.

A schema tell our database client what tables should exist in our database, and 
the datatypes of the fields in the tables.

When defining the tables, we can add constraints on each field like 
`primary_key` for primary keys, `unique` to enforce unique values, and `null` 
to prevent `None` values.

We also can do more complicated things like composite keys and indexes.
"""



"""
We define this database proxy (fake database object) so the base table model 
has a reference to the database. We "swap in" the real database later.

This is just a requirement when using `peewee`, I don't fully understand it, 
but if you do, maybe improve this comment.
"""
_dbProxy = _PW.DatabaseProxy()



# === Define a class to extend when creating the schema for db tables ===

class BaseModel(_PW.Model):
  # This lets us give all the tables some common attributes
  class Meta:
    # This tells each table class what database it's in
    database = _dbProxy
    legacy_table_names = False


# `peewee` removes Meta at runtime, keep a stand-in for type checkers to ignore 
# annoying syntax messages.
if _TYPING.TYPE_CHECKING:
  BaseMeta = BaseModel.Meta
else:
  class BaseMeta:
    pass

# === ===



# === Define some reusable field types ===

# Saves us re-writing common field types

pk_uuid = lambda : _PW.UUIDField(
  primary_key=True,
  default=_UUID.uuid4,
  unique=True,
  null=False,
)
"""Primary Key that generates a random UUID on creation"""

# === ===



# === Define some enums for enum fields ===

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

# === ===


#region Table Schemas
# === Define the table schemas ===

class User(BaseModel):
  """Users of this application"""

  id = pk_uuid()
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

  user = _PW.ForeignKeyField(User,
    backref="permissionGroups",
    on_update="CASCADE",
    on_delete="CASCADE",
  )
  """Entry in `User` table"""

  permissionGroup = _PW.ForeignKeyField(PermissionGroup,
    backref="users",
    on_update="CASCADE",
    on_delete="CASCADE",
  )
  """Entry in `PermissionGroup` table"""

  class Meta(BaseMeta):
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

  id = pk_uuid()
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

  id = pk_uuid()
  """UUID primary key"""

  booking = _PW.ForeignKeyField(Booking,
    backref="tickets",
    on_update="CASCADE",
    on_delete="CASCADE",
  )
  """Entry in `Booking` table"""

  holderName = _PW.CharField(
    max_length=64
  )
  """Optional ticket holder name"""

  holderType = _PW.ForeignKeyField(TicketHolderType,
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

# === ===
#endregion Table Schemas



#region Utils
# === Define some utility classes / subroutines to help use the schema

class Tables:
  User = User
  UserPermissionGroups = UserPermissionGroups
  PermissionGroup = PermissionGroup
  Film = Film
  Booking = Booking
  Ticket = Ticket
  TicketHolderType = TicketHolderType



def initializeProxy(database: _PW.Database):
  """"
  Swaps in" the real database object to the proxy.

  This must be done before creating the tables.
  """
  _dbProxy.initialize(database)


def createTables(database: _PW.Database):
  """
  Initialise the database proxy and create all tables defined in the schema.

  Returns all the tables.
  """

  initializeProxy(database)

  dbInstance = database
  dbInstance.create_tables([
    Tables.User,
    Tables.UserPermissionGroups,
    Tables.PermissionGroup,
    Tables.Film,
    Tables.Booking,
    Tables.Ticket,
    Tables.TicketHolderType
  ])

  return Tables

# === ===
#endregion Utils