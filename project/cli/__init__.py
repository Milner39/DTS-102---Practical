from .utils import Utils as _Utils
from .types import Types as _Types

from project.database import Database as _Database



"""
This script defines the entry point to the command line interface.
"""



def main():

  #region Globals

  global running; running = True

  global user; user = None

  #endregion



  #region Subroutines

  def exit():
    global running; running = False



  def login():

    global user

    user = None

    while user is None:
      username = input("Username: ")
      password = input("Password: ")

      user = _Database.user__dataByAuth(username, password)

      if (user is None):
        print("Username or password incorrect, try again")

      else:
        print(f"Logged in as \"{user["username"]}\"")

      print()

  #endregion



  #region Main

  while running:

    options: _Types.optionDict = {
      "Exit": exit
    }

    if user is None:
      options.update({
        "Login": login,
        "Register": lambda : ""
      })

    else:
      options.update({
        "Switch User": login
      })


    print(user)
    _Utils.optionSelect(options)

  #endregion
