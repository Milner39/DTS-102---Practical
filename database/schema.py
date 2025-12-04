import enum as _ENUM
import uuid as _UUID
import typing as _TYPING

import peewee as _PW



_dbProxy = _PW.DatabaseProxy()


# === Define a class to extend when creating the schema for db tables ===

class BaseModel(_PW.Model):
  class Meta:
    # This tells each table class what database it's in
    database = _dbProxy
    legacy_table_names = False


# Peewee removes Meta at runtime, keep a stand-in for type checkers
if _TYPING.TYPE_CHECKING:
  BaseMeta = BaseModel.Meta
else:
  class BaseMeta:
    pass

# === ===



# === Define some reusable field types ===

# Primary Key that generates a random UUID on creation
pk_uuid = lambda : _PW.UUIDField(
  primary_key=True,
  default=_UUID.uuid4,
  unique=True,
  null=False,
)

# === ===



# === Define some enums for enum fields ===

class PermissionLevels(_ENUM.Enum):
  ADMIN = 0
  DEVELOPER = 1

class TicketHolderTypes(_ENUM.Enum):
  ADULT = 0
  TEENAGER = 1
  CHILD = 2
  STUDENT = 3

# === ===



# === Define the table schemas ===

class User(BaseModel):
  id = pk_uuid()

  # Used to login so must be unique
  username = _PW.CharField(
    max_length=64,
    unique=True,
    null=False,
  )

  # Will be stored as plain-text because encryption is out of scope
  password = _PW.CharField(
    max_length=64,
    null=False,
  )

  contactPhone = _PW.CharField(
    max_length=32,
    null=True,
  )


# Used to show different users special options
class Permission(BaseModel):
  id = _PW.SmallIntegerField(
    primary_key=True,
    unique=True,
    null=False,
  )

  readable = _PW.CharField(
    max_length=32,
    unique=True,
    null=False,
  )


# Join table for users and permissions
class UserPermissions(BaseModel):
  user = _PW.ForeignKeyField(User,
    backref="permissions",
    on_update="CASCADE",
    on_delete="CASCADE",
  )
  permission = _PW.ForeignKeyField(Permission,
    backref="users",
    on_update="CASCADE",
    on_delete="CASCADE",
  )

  class Meta(BaseMeta):
    primary_key = _PW.CompositeKey("user", "permission")


class Film(BaseModel):
  title = _PW.CharField(
    primary_key=True,
    max_length=64,
    unique=True,
    null=False,
  )


class Booking(BaseModel):
  id = pk_uuid()

  user = _PW.ForeignKeyField(User,
    backref="bookings",
    on_update="CASCADE"
    # Do not delete bookings if the user has been deleted
  )

  film = _PW.ForeignKeyField(Film,
    backref="bookings",
    on_update="CASCADE",
    on_delete="CASCADE",
  )

  datetime = _PW.DateTimeField(
    null=False
  )


class TicketHolderType(BaseModel):
  id = _PW.SmallIntegerField(
    primary_key=True,
    unique=True,
    null=False,
  )

  readable = _PW.CharField(
    max_length=32,
    unique=True,
    null=False,
  )


class Ticket(BaseModel):
  id = pk_uuid()

  booking = _PW.ForeignKeyField(Booking,
    backref="tickets",
    on_update="CASCADE",
    on_delete="CASCADE",
  )

  # Optional ticket holder name
  holderName = _PW.CharField(
    max_length=64
  )

  holderType = _PW.ForeignKeyField(TicketHolderType,
    backref="tickets",
  )

  # In case refunds are made
  paidPriceGBP = _PW.DecimalField(
    max_digits=5,
    decimal_places=2,
    auto_round=True,
    null=False
  )

# === ===



def initializeProxy(database: _PW.Database):
  _dbProxy.initialize(database)

def createTables(database: _PW.Database):
  initializeProxy(database)

  class Tables:
    User = User
    UserPermissions = UserPermissions
    Permission = Permission
    Film = Film
    Booking = Booking
    Ticket = Ticket
    TicketHolderType = TicketHolderType

  dbInstance = database
  dbInstance.create_tables([
    Tables.User,
    Tables.UserPermissions,
    Tables.Permission,
    Tables.Film,
    Tables.Booking,
    Tables.Ticket,
    Tables.TicketHolderType
  ])

  return Tables