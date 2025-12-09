# repository.py
from typing import List, Optional, Dict
from database.db_connection import execute_query, fetch_query
from database.models import User, Favourite, HistoryEntry
# ---------------------
# Initialization helper
# ---------------------
def init_db_from_schema(schema_path: str = "database/schema.sql") -> None:
    """
    Run the schema.sql file to create tables if they don't exist.
    Call once at setup or program start if desired.
    """
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()
    # execute script using sqlite3 directly (bypassing helpers)
    import sqlite3
    from database.config import DB_PATH
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()
# ---------------------
# USERS
# ---------------------
def add_user(user: User) -> int:
    query = "INSERT INTO users (username, email) VALUES (?, ?)"
    params = (user.username, user.email)
    return execute_query(query, params)
def get_users() -> List[Dict]:
    query = "SELECT * FROM users ORDER BY id"
    return fetch_query(query)
def get_user_by_email(email: str) -> Optional[Dict]:
    query = "SELECT * FROM users WHERE email = ?"
    results = fetch_query(query, (email,))
    return results[0] if results else None
# ---------------------
# FAVOURITES
# ---------------------
def add_favourite(fav: Favourite) -> int:
    query = """
    INSERT INTO favourites (user_id, movie_id, title, media_type, genre, rating)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    params = (fav.user_id, fav.movie_id, fav.title, fav.media_type, fav.genre, fav.rating)
    return execute_query(query, params)
def get_favourites_by_user(user_id: int) -> List[Dict]:
    query = "SELECT * FROM favourites WHERE user_id = ? ORDER BY added_at DESC"
    return fetch_query(query, (user_id,))
def delete_favourite(fav_id: int) -> None:
    query = "DELETE FROM favourites WHERE id = ?"
    execute_query(query, (fav_id,))
def find_favourite(user_id: int, movie_id: str) -> Optional[Dict]:
    query = "SELECT * FROM favourites WHERE user_id = ? AND movie_id = ?"
    results = fetch_query(query, (user_id, movie_id))
    return results[0] if results else None
# ---------------------
# HISTORY
# ---------------------
def add_history(entry: HistoryEntry) -> int:
    query = "INSERT INTO history (user_id, search_keyword) VALUES (?, ?)"
    params = (entry.user_id, entry.search_keyword)
    return execute_query(query, params)
def get_history_by_user(user_id: int) -> List[Dict]:
    query = "SELECT * FROM history WHERE user_id = ? ORDER BY searched_at DESC"
    return fetch_query(query, (user_id,))
def clear_history_by_user(user_id: int) -> None:
    query = "DELETE FROM history WHERE user_id = ?"
    execute_query(query, (user_id,))