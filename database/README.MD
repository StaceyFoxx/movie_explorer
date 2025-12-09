# Database Module (SQLite) — Movie Explorer

## Overview
This module handles all local database operations for the Movie Explorer console app. It uses SQLite and stores data in a single file (`movie_app.db`). The database stores users, favourites (with rating and genre), and search history.

## Files (database/)
`__init__.py` — package exports
`config.py` — DB path (`DB_PATH = "movie_app.db"`)
`db_connection.py` — connection & helper functions (`execute_query`, `fetch_query`)
`models.py` — dataclasses: `User`, `Favourite`, HistoryEntry
`repository.py` — CRUD functions and init_db_from_schema
`schema.sql` — SQL to create tables
## Quick setup
(Optional) Copy `database/schema.sql` to the `database/` folder.
Run the schema once (either with the app calling `init_db_from_schema()` or manually):
Manual: sqlite3 movie_app.db < database/schema.sql
Python: call from database.repository import init_db_from_schema; init_db_from_schema()
Install Python dependencies (none required for sqlite; just standard library). If you use extras, list them in project README.
## Example usage
```python
from database import (
    add_user, get_users, add_favourite, get_favourites_by_user,
    add_history, get_history_by_user, find_favourite
)
from database.models import User, Favourite, HistoryEntry

# create a user
user_id = add_user(User(id=None, username="alice", email="alice@example.com"))

# add favourite
fav = Favourite(id=None, user_id=user_id, movie_id="550", title="Fight Club", media_type="movie",
                genre="Drama", rating=4.5)
add_favourite(fav)

# check favourites
print(get_favourites_by_user(user_id))

# add search history
add_history(HistoryEntry(id=None, user_id=user_id, search_keyword="fight club"))

# read history
print(get_history_by_user(user_id))
