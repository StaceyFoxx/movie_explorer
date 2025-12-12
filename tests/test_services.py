import unittest
from unittest import mock
from services.favorites_service import FavouritesService
from services.search_service import SearchService
from services.recommendation_service import RecommendationService
from api.tmdb_client import TMDbClient
from models.movie import Movie

# -----------------------------
# FavouritesService Tests
# -----------------------------
class TestFavouritesService(unittest.TestCase):

    def setUp(self):
        self.fav_service = FavouritesService()
        self.user_id = 1
        self.movie_id = "m123"
        self.title = "Inception"

        # Patch repository methods
        self.patcher_find = mock.patch("database.repository.find_favourite")
        self.patcher_add = mock.patch("database.repository.add_favourite")
        self.patcher_delete = mock.patch("database.repository.delete_favourite")
        self.mock_find = self.patcher_find.start()
        self.mock_add = self.patcher_add.start()
        self.mock_delete = self.patcher_delete.start()

    def tearDown(self):
        mock.patch.stopall()

    def test_add_favourite_new(self):
        self.mock_find.return_value = None
        self.mock_add.return_value = 42
        fav_id = self.fav_service.add_favourite(self.user_id, self.movie_id, self.title, "movie")
        self.assertEqual(fav_id, 42)
        self.mock_add.assert_called_once()

    def test_add_favourite_existing(self):
        self.mock_find.return_value = {"id": 99}
        fav_id = self.fav_service.add_favourite(self.user_id, self.movie_id, self.title, "movie")
        self.assertEqual(fav_id, 99)
        self.mock_add.assert_not_called()

    def test_remove_favourite_by_movie_id(self):
        self.mock_find.return_value = {"id": 101}
        result = self.fav_service.remove_favourite_by_movie_id(self.user_id, self.movie_id)
        self.assertTrue(result)
        self.mock_delete.assert_called_once_with(101)


# -----------------------------
# SearchService Tests
# -----------------------------
class TestSearchService(unittest.TestCase):

    def setUp(self):
        self.mock_tmdb = mock.Mock(spec=TMDbClient)
        self.search_service = SearchService(self.mock_tmdb)
        self.user_id = 1

        # Patch repository method for logging history
        self.patcher_add_history = mock.patch("database.repository.add_history")
        self.mock_add_history = self.patcher_add_history.start()

        # Mock _map_tmdb_to_movie to avoid calling Movie constructor incorrectly
        self.search_service._map_tmdb_to_movie = mock.Mock(
            side_effect=lambda data: Movie(id=str(data["id"]), title=data["title"])
        )

    def tearDown(self):
        mock.patch.stopall()

    def test_search_movies_logs_history_and_returns_movies(self):
        self.mock_add_history.return_value = 1
        self.mock_tmdb.search_movie.return_value = {
            "results": [{"id": "123", "title": "Inception"}]
        }
        results = self.search_service.search_movies(self.user_id, "Inception")
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], Movie)
        self.mock_add_history.assert_called_once()

    def test_search_movies_empty_keyword(self):
        results = self.search_service.search_movies(self.user_id, "")
        self.assertEqual(results, [])


# -----------------------------
# RecommendationService Tests
# -----------------------------
class TestRecommendationService(unittest.TestCase):

    def setUp(self):
        self.mock_tmdb = mock.Mock(spec=TMDbClient)
        self.recommend_service = RecommendationService(self.mock_tmdb)

        # Patch _map_tmdb_to_movie to avoid constructor errors
        self.recommend_service._search_service._map_tmdb_to_movie = mock.Mock(
            side_effect=lambda data: Movie(id=str(data["id"]), title=data["title"])
        )

    def test_get_trending_recommendations(self):
        self.mock_tmdb.get_trending_movies.return_value = {
            "results": [{"id": "1", "title": "Inception"}]
        }
        movies = self.recommend_service.get_trending_recommendations()
        self.assertEqual(len(movies), 1)
        self.assertIsInstance(movies[0], Movie)
        self.assertEqual(movies[0].title, "Inception")


if __name__ == "__main__":
    unittest.main()