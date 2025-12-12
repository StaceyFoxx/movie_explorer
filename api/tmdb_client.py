# api/tmdb_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TMDbClient:
    """
    A simple OOP client for TMDb API.
    Handles searching, movie details, and trending movies.
    """

    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        if not self.api_key:
            raise ValueError("TMDB_API_KEY not found in environment variables (.env).")

    # ------------------------------
    # Internal request helper
    # ------------------------------
    def _make_request(self, endpoint: str, params: dict = None) -> dict | None:
        """
        Internal helper to perform GET requests.
        """
        url = f"{self.BASE_URL}{endpoint}"
        params = params or {}
        params["api_key"] = self.api_key

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"TMDb request failed: {e}")
            return None

    # ------------------------------
    # Public API methods
    # ------------------------------
    def search_movie(self, query: str) -> dict | None:
        """
        Search for a movie by name.
        Returns JSON or None.
        """
        return self._make_request("/search/movie", {"query": query})

    def get_movie_details(self, movie_id: int) -> dict | None:
        """
        Fetch full details for a movie.
        """
        return self._make_request(f"/movie/{movie_id}")

    def get_trending_movies(self) -> dict | None:
        """
        Fetch trending movies for the day.
        """
        return self._make_request("/trending/movie/day")

