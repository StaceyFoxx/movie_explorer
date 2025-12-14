import unittest
from unittest import mock
from services.favorites_service import FavouritesService
from services.search_service import SearchService
from services.recommendation_service import RecommendationService
from api.tmdb_client import TMDbClient
from models.movie import Movie


class TestFavouritesService(unittest.TestCase):
    """
    Tests adding, fetching, and removing favourite movies for a user.
    """

    def setUp(self):
        """
        Sets up FavouritesService instance and mocks repository methods.

        This runs before each test to ensure a clean environment.
        """
        # creates FavouritesService instance
        self.fav_service = FavouritesService()

        # example user and movie data
        self.user_id = 1
        self.movie_id = "m101"
        self.title = "The Matrix"

        # mocks repository methods to prevent real DB calls
        self.patcher_find = mock.patch("database.repository.find_favourite")
        self.patcher_add = mock.patch("database.repository.add_favourite")
        self.patcher_delete = mock.patch("database.repository.delete_favourite")
        self.mock_find = self.patcher_find.start()
        self.mock_add = self.patcher_add.start()
        self.mock_delete = self.patcher_delete.start()

    def tearDown(self):
        """
        Stops all mocks after each test.
        """
        mock.patch.stopall()

    def test_add_favourite_new(self):
        """
        Tests adding new favourite movie.

        Checks new favourite is added and if correct ID is returned.
        """
        self.mock_find.return_value = None
        self.mock_add.return_value = 101

        fav_id = self.fav_service.add_favourite(self.user_id, self.movie_id, self.title, "movie")
        self.assertEqual(fav_id, 101)
        self.mock_add.assert_called_once()

    def test_add_favourite_existing(self):
        """
        Tests adding favourite which already exists.

        It should not add duplicate and should return existing ID.
        """
        self.mock_find.return_value = {"id": 202}

        fav_id = self.fav_service.add_favourite(self.user_id, self.movie_id, self.title, "movie")
        self.assertEqual(fav_id, 202)
        self.mock_add.assert_not_called()

    def test_remove_favourite_by_movie_id(self):
        """
        Tests removing favourite movie by movie ID.

        Checks delete method is called with correct ID.
        """
        self.mock_find.return_value = {"id": 303}

        result = self.fav_service.remove_favourite_by_movie_id(self.user_id, self.movie_id)
        self.assertTrue(result)
        self.mock_delete.assert_called_once_with(303)


class TestSearchService(unittest.TestCase):
    """
    Tests searching movies via TMDb and logging search history.
    """

    def setUp(self):
        """
        Sets up SearchService with mocked TMDb client.

        Also mocks add_history to prevent affecting real DB.
        """
        self.mock_tmdb = mock.Mock(spec=TMDbClient)
        self.search_service = SearchService(self.mock_tmdb)
        self.user_id = 1

        self.patcher_add_history = mock.patch("database.repository.add_history")
        self.mock_add_history = self.patcher_add_history.start()

        self.search_service._map_tmdb_to_movie = mock.Mock(
            side_effect=lambda data: Movie(id=str(data["id"]), title=data["title"])
        )

    def tearDown(self):
        """Stops all mocks after each test."""
        mock.patch.stopall()

    def test_search_movies_logs_history_and_returns_movies(self):
        """
        Tests searching for movies with keyword.

        Ensures TMDb is called, a Movie object is returned, and search is logged.
        """
        self.mock_add_history.return_value = 1
        self.mock_tmdb.search_movie.return_value = {
            "results": [{"id": "201", "title": "Avengers: Endgame"}]
        }

        results = self.search_service.search_movies(self.user_id, "Avengers")
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], Movie)
        self.mock_add_history.assert_called_once()

    def test_search_movies_empty_keyword(self):
        """
        Tests searching with empty keyword.

        Should return empty list and not call TMDb or log history.
        """
        results = self.search_service.search_movies(self.user_id, "")
        self.assertEqual(results, [])


class TestRecommendationService(unittest.TestCase):
    """
    Tests fetching trending movie recommendations.
    """

    def setUp(self):
        """
        Sets up RecommendationService with mocked TMDb client.

        Also mocks mapping to Movie objects to prevent constructor issues
        or needing to rely on the API.
        """
        self.mock_tmdb = mock.Mock(spec=TMDbClient)
        self.recommend_service = RecommendationService(self.mock_tmdb)

        self.recommend_service._search_service._map_tmdb_to_movie = mock.Mock(
            side_effect=lambda data: Movie(id=str(data["id"]), title=data["title"])
        )

    def test_get_trending_recommendations(self):
        """
        Tests fetching trending movies from TMDb.

        Ensures results are Movie objects and titles match mocked data.
        """
        self.mock_tmdb.get_trending_movies.return_value = {
            "results": [{"id": "301", "title": "Spider-Man: No Way Home"}]
        }

        movies = self.recommend_service.get_trending_recommendations()
        self.assertEqual(len(movies), 1)
        self.assertIsInstance(movies[0], Movie)
        self.assertEqual(movies[0].title, "Spider-Man: No Way Home")


if __name__ == "__main__":
    unittest.main()