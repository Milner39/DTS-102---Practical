class QueryExceptions():

  class EntryNotFound(Exception):
    pass

  class EntryAlreadyExists(Exception):
    pass

  class EntryDoesNotMatch(Exception):
    pass

  class MultipleEntriesFound(Exception):
    pass