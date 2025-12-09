# models.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    created_at: Optional[str] = None


@dataclass
class Favourite:
    id: Optional[int]
    user_id: int
    movie_id: str
    title: str
    media_type: str          # 'movie' or 'tv'
    genre: Optional[str] = None
    rating: Optional[float] = None
    added_at: Optional[str] = None


@dataclass
class HistoryEntry:
    id: Optional[int]
    user_id: int
    search_keyword: str
    searched_at: Optional[str] = None
