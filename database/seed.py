from client import DBClient

dbClient = DBClient()


filmTitles = [
  "Jurassic Cabin",
  "The Dark Night",
  "The Nightmare on First Street",
  "Quantum Mania",
  "The Game of Thorns",
  "The Shape of Time"
]

for filmTitle in filmTitles:
  dbClient.tables.Film.get_or_create(
    title=filmTitle
  )