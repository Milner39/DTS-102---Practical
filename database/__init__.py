from enum import Enum
from typing import TYPE_CHECKING

# Database ORM
import peewee as PW
import peewee_enum_field as PWE

# Random Ids
import uuid



db = PW.SqliteDatabase("database/data.db", pragmas={ "foreign_keys": 1 })


# === Define a class to extend when creating the schema for db tables ===

class BaseModel(PW.Model):
  class Meta:
    # This tells each table class what database it's in
    database = db
    legacy_table_names = False


# Peewee removes Meta at runtime, keep a stand-in for type checkers
if TYPE_CHECKING:
  BaseMeta = BaseModel.Meta
else:
  class BaseMeta:
    pass

# === Define a class to extend when creating the schema for db tables ===



# === Define some reusable field types ===

# Primary Key that generates a random UUID on creation
pk_uuid = PW.UUIDField(
  primary_key=True,
  default=uuid.uuid4,
  unique=True,
  null=False,
)

# === Define some reusable field types ===



# === Define some enums for enum fields ===

class ENUM__Permission_level(Enum):
  ADMIN = 0
  DEVELOPER = 1

class ENUM__Ticket_holderType(Enum):
  ADULT = 0
  TEENAGER = 1
  CHILD = 2
  STUDENT = 3

# === Define some enums for enum fields ===



# === Define the table schemas ===

class User(BaseModel):
  id = pk_uuid

  # Used to login so must be unique
  username = PW.CharField(
    max_length=64,
    unique=True,
    null=False,
  )

  # Will be stored as plain-text because encryption is out of scope
  password = PW.CharField(
    max_length=64,
    null=False,
  )

  contactPhone = PW.CharField(
    max_length=32,
  )


# Used to show different users special options
class Permission(BaseModel):
  level = PWE.EnumField(ENUM__Permission_level,
    primary_key=True,
    max_length=32,
    unique=True,
    null=False,
  )


# Join table for users and permissions
class UserPermissions(BaseModel):
  user = PW.ForeignKeyField(User,
    backref="permissions",
    on_update="CASCADE",
    on_delete="CASCADE",
  )
  permission = PW.ForeignKeyField(Permission,
    backref="users",
    on_update="CASCADE",
    on_delete="CASCADE",
  )

  class Meta(BaseMeta):
    primary_key = PW.CompositeKey("user", "permission")


class Film(BaseModel):
  title = PW.CharField(
    primary_key=True,
    max_length=64,
    unique=True,
    null=False,
  )


class Booking(BaseModel):
  id = pk_uuid

  user = PW.ForeignKeyField(User,
    backref="bookings",
    on_update="CASCADE"
    # Do not delete bookings if the user has been deleted
  )

  film = PW.ForeignKeyField(Film,
    backref="bookings",
    on_update="CASCADE",
    on_delete="CASCADE",
  )

  datetime = PW.DateTimeField()


class Ticket(BaseModel):
  id = pk_uuid

  booking = PW.ForeignKeyField(Booking,
    backref="tickets",
    on_update="CASCADE",
    on_delete="CASCADE",
  )

  # Optional ticket holder name
  holderName = PW.CharField(
    max_length=64
  )

  holderType = PWE.EnumField(ENUM__Ticket_holderType,
    max_length=32,
    null=False,
  )

  # In case refunds are made
  paidPriceGBP = PW.DecimalField(
    max_digits=5,
    decimal_places=2,
    auto_round=True,
    null=False
  )

# === Define the table schemas ===



# === Create the tables ===

db.connect()

class Tables:
  User = User
  UserPermissions = UserPermissions
  Permission = Permission
  Film = Film
  Booking = Booking
  Ticket = Ticket

db.create_tables([
  Tables.User,
  Tables.UserPermissions,
  Tables.Permission,
  Tables.Film,
  Tables.Booking,
  Tables.Ticket
])

# === Create the tables ===