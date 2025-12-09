# db_connection.py
import sqlite3
from typing import Optional
from database.config import DB_PATH

def get_connection() -> sqlite3.Connection:
    """
    Return a SQLite connection with row factory set to return sqlite3.Row objects
    (which behave like dicts).
    """
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    # enforce foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def execute_query(query: str, params: tuple = None) -> int:
    """
    Execute a write query. Returns lastrowid.
    """
    params = params or ()
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def fetch_query(query: str, params: tuple = None):
    """
    Execute a read query and return list of dicts.
    """
    params = params or ()
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()