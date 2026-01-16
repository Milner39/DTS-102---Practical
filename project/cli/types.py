import typing as _TYPING



"""This script defines some types for the cli module"""



#region Types

class Types:

  optionDict = dict[str, _TYPING.Callable]
  optionList = list[tuple[str, _TYPING.Callable]]

#region
