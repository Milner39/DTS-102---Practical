import enum as _ENUM



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

#endregion