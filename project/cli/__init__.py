from datetime import datetime as _DT

from .utils import Utils as _Utils
from .format import Format as _Format
from .types import Types as _Types

from project.database import Database as _Database



"""
This script defines the entry point to the command line interface.
"""



def main():
  """Entry point to the cli"""

  #region Globals

  global running; running = True

  global user; user = None

  #endregion



  #region Subroutines

  def exit():
    """Stop the cli"""
    global running; running = False



  def login():
    """User logs in with username and password."""

    global user; user = None

    while user is None:
      username = input("Username: ")
      password = input("Password: ")

      user = _Database.user__dataByAuth(username, password)

      if (user is None):
        print("Username or password incorrect, try again")

      else:
        print(f"Logged in as \"{user["username"]}\"")

      print()



  def register():
    """User logs in with new username and password."""

    global user; user = None

    while user is None:
      username = input("Username: ")
      password = input("Password: ")

      user = _Database.user__register(username, password)

      if (user is None):
        print("Username is taken, try again")

      else:
        print(f"Logged in as \"{user["username"]}\"")

      print()



  def createBooking():
    """Create a new booking."""

    global user
    if user is None: raise


    def createTickets(filmTitle: str):
      tickets = []

      ticketOptions = {
        "Finish": lambda: None
      }
      
      for ticketType in _Database.ticketHolderType__allTypes():
        ticketOptions[ticketType.title()] = lambda t=ticketType: t

      while True:
        tType = _Utils.optionSelect(ticketOptions)
        if tType is None: break
        else: tickets.append(tType)

      return (filmTitle, tickets)


    datetime: _DT | None = None
    while datetime is None:
      # TODO: account for current datetime (prevent bookings before today)
      try:
        dateStr = input("Enter booing date and time (DD/MM/YYYY HH:MM): ")
        datetime = _DT.strptime(dateStr, "%d/%m/%Y %H:%M")
      except ValueError:
        print("Invalid datetime, try again")
    print()

    filmOptions = {}
    for title in _Database.film__allTitles():
      filmOptions[title] = lambda t=title: createTickets(t)

    print("Select a film")
    filmTitle, tickets = _Utils.optionSelect(filmOptions)
    if len(tickets) == 0: return

    _Database.booking__create(user["id"], datetime, filmTitle, tickets)



  def viewUserBookings():
    """View the user's booking bookings."""

    global user
    if user is None: raise

    bookings = _Database.booking__getByUserId(user["id"])
    if len(bookings) < 1:
      print("You haven't make any bookings yet.")
    else:
      print(_Format.bookingsTable(bookings))
    print()



  def viewAllBookings():
    """View all bookings."""

    global user
    if user is None: raise
    if "ADMIN" not in user["permissionGroups"]: raise

    bookings = _Database.booking__getAll()
    if len(bookings) < 1:
      print("There aren't any bookings yet.")
    else:
      print(_Format.bookingsTable(bookings))
    print()

  #endregion



  #region Main Loop

  while running:

    options: _Types.optionDict = {
      "Exit": exit
    }

    if user is None:
      options.update({
        "Login": login,
        "Register": register
      })

    else:
      options.update({
        "Switch User": login,
      })

      if ("ADMIN" in user["permissionGroups"]):
        options.update({
          "View all bookings": viewAllBookings
        })

      options.update({
        "View your bookings": viewUserBookings,
        "Create a booking": createBooking
      })


    _Utils.optionSelect(options)

  #endregion
