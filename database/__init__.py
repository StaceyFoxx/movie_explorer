# __init__.py
from .db_connection import get_connection, execute_query, fetch_query
from .models import User, Favourite, HistoryEntry
from .repository import (
    init_db_from_schema,
    add_user, get_users, get_user_by_email,
    add_favourite, get_favourites_by_user, delete_favourite, find_favourite,
    add_history, get_history_by_user, clear_history_by_user
)

__all__ = [
    "get_connection", "execute_query", "fetch_query",
    "User", "Favourite", "HistoryEntry",
    "init_db_from_schema",
    "add_user", "get_users", "get_user_by_email",
    "add_favourite", "get_favourites_by_user", "delete_favourite", "find_favourite",
    "add_history", "get_history_by_user", "clear_history_by_user"
]
