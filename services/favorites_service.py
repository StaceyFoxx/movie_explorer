from typing import List, Dict, Optional
from database import repository
from database.models import Favourite


class FavouritesService:
    """Manages the addition, retrieval, and removal of user favourites."""

    def add_favourite(self, user_id: int, movie_id: str, title: str, media_type: str, genre: Optional[str] = None,
                      rating: Optional[float] = None) -> int:
        """
        Adds a new favourite to the database.

        Returns the ID of the newly added favourite, or the existing ID if it already exists.
        """
        # Note: repository.find_favourite is used here
        existing_fav = repository.find_favourite(user_id, movie_id)
        if existing_fav:
            print(f"Item {movie_id} already favourited by user {user_id}")
            return existing_fav['id']

        fav = Favourite(
            id=None,  # ID is auto-generated
            user_id=user_id,
            movie_id=movie_id,
            title=title,
            media_type=media_type,
            genre=genre,
            rating=rating
        )
        return repository.add_favourite(fav)

    def get_user_favourites(self, user_id: int) -> List[Dict]:
        """Retrieves all favourites for a given user, ordered by most recently added."""
        return repository.get_favourites_by_user(user_id)

    def remove_favourite_by_id(self, fav_id: int) -> None:
        """Removes a favourite item by its database ID."""
        repository.delete_favourite(fav_id)

    def remove_favourite_by_movie_id(self, user_id: int, movie_id: str) -> bool:
        """Removes a favourite item by user_id and movie_id."""
        existing_fav = repository.find_favourite(user_id, movie_id)
        if existing_fav:
            repository.delete_favourite(existing_fav['id'])
            return True
        return False

    def is_favourite(self, user_id: int, movie_id: str) -> bool:
        """Checks if a media item is already favourited by a user."""
        return repository.find_favourite(user_id, movie_id) is not None