from typing import List, Dict, Any
from api.tmdb_client import TMDbClient
from database import repository
from database.models import HistoryEntry
from models.movie import Movie


class SearchService:
    """Handles searching media via TMDb and managing user search history."""

    def __init__(self, tmdb_client: TMDbClient):
        self._tmdb_client = tmdb_client

    # ------------------
    # Search Operations
    # ------------------

    def search_movies(self, user_id: int, keyword: str) -> List[Movie]:
        """
        Searches TMDb for movies, logs the search keyword, and returns a list of Movie models.
        """
        if not keyword:
            return []

        # 1. Log the search history
        self.log_search_history(user_id, keyword)

        # 2. Search TMDb
        tmdb_results = self._tmdb_client.search_movie(keyword)

        if not tmdb_results or 'results' not in tmdb_results:
            return []

        # 3. Process results into Movie models
        movies: List[Movie] = []
        for result in tmdb_results.get('results', []):
            # Only process results that are likely movies (have a title/release date)
            if 'title' in result:
                movie = self._map_tmdb_to_movie(result)
                movies.append(movie)

        return movies

    def get_movie_details(self, movie_id: int) -> Movie | None:
        """Fetches detailed information for a single movie ID."""
        details = self._tmdb_client.get_movie_details(movie_id)
        if details:
            return self._map_tmdb_to_movie(details)
        return None

    def _map_tmdb_to_movie(self, data: Dict[str, Any]) -> Movie:
        """Maps raw TMDb data dictionary to a Movie model."""

        # TMDb genre details can come as a list of IDs (search) or a list of dicts (details)
        genres_list = data.get('genres', [])
        if not genres_list and data.get('genre_ids'):
            # Handle genre IDs from search endpoint. (Requires a separate lookup/cache for names)
            genres_display = [str(g) for g in data.get('genre_ids')]
        else:
            # Handle genre names from details endpoint
            genres_display = [g['name'] for g in genres_list if 'name' in g]

        return Movie(
            id=str(data.get('id')),
            title=data.get('title', data.get('name', 'N/A')),  # Fallback to 'name' for TV/mixed results
            overview=data.get('overview', 'No overview available.'),
            poster_path=data.get('poster_path'),
            release_date=data.get('release_date'),
            vote_average=data.get('vote_average', 0.0),
            genres=genres_display,
            media_type="movie"
        )

    # ------------------
    # History Management
    # ------------------

    def log_search_history(self, user_id: int, keyword: str) -> int:
        """Adds a search keyword to the user's history."""
        entry = HistoryEntry(id=None, user_id=user_id, search_keyword=keyword.strip())
        return repository.add_history(entry)

    def get_user_history(self, user_id: int) -> List[Dict]:
        """Retrieves a user's search history, ordered by most recent."""
        return repository.get_history_by_user(user_id)

    def clear_user_history(self, user_id: int) -> None:
        """Deletes all search history for a user."""
        repository.clear_history_by_id(user_id)