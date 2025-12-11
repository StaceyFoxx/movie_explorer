"""
Utilities for formatting media items and related data
for console display.
"""

from typing import Iterable, Optional, List

from models import MediaItem  # This is models.__init__ re‑exporting MediaItem


def truncate_text(text: str, max_length: int = 80) -> str:
    """
    Truncate text to at most `max_length` characters, adding "..."
    if it was cut.
    """
    if text is None:
        return ""
    text = str(text)
    if len(text) <= max_length:
        return text
    # keep space for "..."
    return text[: max_length - 3].rstrip() + "..."


def format_genres(genres: Optional[Iterable[str]]) -> str:
    """
    Turn a list of genre names into a comma‑separated string.
    """
    if not genres:
        return "Unknown"
    return ", ".join(str(g) for g in genres)


def format_rating(rating: Optional[float]) -> str:
    """
    Format a numeric rating as 'X.Y/10' or 'No rating'.
    """
    if rating is None:
        return "No rating"
    try:
        return f"{float(rating):.1f}/10"
    except (TypeError, ValueError):
        return "No rating"


def format_media_item(item: MediaItem, index: Optional[int] = None) -> str:
    """
    Format a single MediaItem (Movie or TVShow) as one line of text.

    Uses:
    - item.id
    - item.title
    - item.media_type
    - item.genres
    - item.rating
    """
    prefix = f"{index}. " if index is not None else ""
    title = truncate_text(item.title, 60)
    genres = format_genres(getattr(item, "genres", []))
    rating = format_rating(getattr(item, "rating", None))
    media_type = getattr(item, "media_type", "unknown")

    return f"{prefix}[{media_type}] {title} | Genres: {genres} | Rating: {rating}"


def format_media_list(items: Iterable[MediaItem]) -> str:
    """
    Format a list of MediaItem objects into multiple lines of text.
    """
    lines: List[str] = []
    for idx, item in enumerate(items, start=1):
        lines.append(format_media_item(item, index=idx))
    if not lines:
        return "No results found."
    return "\n".join(lines)
