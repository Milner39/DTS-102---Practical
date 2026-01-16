from .types import Types as _Types



"""This script defines some utilities for the cli module"""



#region Utils

class Utils:

  @staticmethod
  def optionsDictToList(options: _Types.optionDict) -> _Types.optionList:
    """
    Converts an option dictionary like this:
    ```python
      options = {
        "DoFoo": fooFunc,
        "DoBar": barFunc
      }
    ```

    To an option list like this:
    ```python
      options = [
        ["DoFoo", fooFunc],
        ["DoBar", barFunc]
      ]
    ```
    """

    optList = [(optName, optFunc) for optName, optFunc in options.items()]
    return optList


  @staticmethod
  def optionSelect(options: _Types.optionDict):
    """
    Takes an option dictionary and prints a CLI prompt where users can select 
    the numbered options.

    Returns the output of the option function.
    """

    optList = __class__.optionsDictToList(options)
    """List of tuples containing the option name and the option function"""


    def isValid(optInput):
      """Returns `True` if the input is a valid option in `optList`"""

      try:
        optInput = int(optInput)
      except:
        return False

      return (
        optInput >= 0 and 
        optInput < len(optList)
      )

    # Get a valid options from the user
    selectedOpt: str | None = None
    while (not isValid(selectedOpt)):
      for i, opt in enumerate(optList):
        print(f"[{i}] {opt[0]}")

      selectedOpt = input("> ")

      if (not isValid(selectedOpt)):
        print("Invalid option, try again")

      print()

    # Return the result of the selected option function
    assert selectedOpt is not None
    return optList[int(selectedOpt)][1]()

#region
