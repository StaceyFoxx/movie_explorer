import unittest
from unittest import mock
from api.tmdb_client import TMDbClient


class TestTMDbClient(unittest.TestCase):
    """
    Tests TMDb client methods without hitting the real API
    and avoiding real network calls.

    Mocking is used to simulate API responses.
    """

    def setUp(self):
        """
        Creates TMDbClient instance before each test.

        Allows for each test to have a fresh client to work with.
        """
        # creates TMDbClient instance
        self.client = TMDbClient()

    @mock.patch.object(TMDbClient, "_make_request")
    def test_search_movie_returns_results(self, mock_request):
        """
        Tests searching movies returns results in expected format.
        """
        # mocks internal _make_request method
        mock_request.return_value = {"results": [{"id": 1, "title": "The Matrix"}]}

        # performs search
        result = self.client.search_movie("Matrix")

        # checks results key exists
        self.assertIn("results", result)

        # checks there's at least one result
        self.assertGreater(len(result["results"]), 0)

        # checks if title matches mocked data
        self.assertEqual(result["results"][0]["title"], "The Matrix")

    @mock.patch.object(TMDbClient, "_make_request")
    def test_get_movie_details_returns_movie(self, mock_request):
        """
        Tests fetching movie details returns correct data structure.
        """
        mock_request.return_value = {"id": 1, "title": "Inception", "media_type": "movie"}

        # gets movie details
        movie = self.client.get_movie_details(1)

        # checks returned data matches mocked values
        self.assertEqual(movie["id"], 1)
        self.assertEqual(movie["title"], "Inception")
        self.assertEqual(movie["media_type"], "movie")

    @mock.patch.object(TMDbClient, "_make_request")
    def test_get_trending_movies_returns_list(self, mock_request):
        """
        Tests fetching trending movies returns a list of movies
        and ensures results are correctly handled.
        """
        mock_request.return_value = {"results": [{"id": 1, "title": "Spider-Man: No Way Home"}]}

        # gets trending movies
        trending = self.client.get_trending_movies()

        # checks results key exists
        self.assertIn("results", trending)

        # checks at least one movie is returned
        self.assertGreater(len(trending["results"]), 0)

        # checks title matches mocked data
        self.assertEqual(trending["results"][0]["title"], "Spider-Man: No Way Home")


if __name__ == "__main__":
    unittest.main()