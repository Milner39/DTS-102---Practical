# Requirements
- Have UV installed

# How To Use
- You may need to run `pip install -e .` if not using UV.
- Run `./database/seed.py` with `uv run -m project.database.seed`.
- Run `./main.py` with `uv run -m project`.
- Install the "qwtel.sqlite-viewer" vscode extension to see how data is stored 
  in normalised tables in the `/project/database/data.db` file.

# Features
- Register user account

- Login as user

- Login as an Admin user with:
  - password: "admin"
  - username: "123"

- Users can create bookings
  - Bookings can have any number of tickets of 4 ticket types

- Users can view THEIR OWN bookings

- Admin users can view ALL bookings

# Notes
- If you are examining this assignment, please look in the `project.database` 
  module for description comments and good coding practices, as the 
  `projects.cli` module was quite rushed (down to the last hour before the 
  deadline)
