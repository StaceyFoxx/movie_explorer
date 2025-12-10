from typing import List
from api.tmdb_client import TMDbClient
from models.movie import Movie
from .search_service import SearchService

class RecommendationService:
    """
    Handles generating media recommendations, currently based on trending data.
    """

    def __init__(self, tmdb_client: TMDbClient):
        self._tmdb_client = tmdb_client
        # We instantiate SearchService here to reuse its internal mapping logic
        self._search_service = SearchService(tmdb_client)

    def get_trending_recommendations(self) -> List[Movie]:
        """
        Fetches the current daily trending movies from TMDb as recommendations.
        """
        tmdb_results = self._tmdb_client.get_trending_movies()

        if not tmdb_results or 'results' not in tmdb_results:
            return []

        movies: List[Movie] = []
        for result in tmdb_results.get('results', []):
            # Only process if it's explicitly a movie or has movie-like properties
            if result.get('media_type') == 'movie' or 'title' in result:
                # Use the private mapping logic from SearchService
                movie = self._search_service._map_tmdb_to_movie(result)
                movies.append(movie)

        return movies