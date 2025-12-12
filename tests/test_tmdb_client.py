import unittest
from api.tmdb_client import TMDbClient

class TestTMDbClient(unittest.TestCase):
    def setUp(self):
        self.client = TMDbClient()

    def test_search_movie_returns_results(self):
        result = self.client.search_movie("Inception")
        self.assertIn("results", result)
        self.assertGreater(len(result["results"]), 0)
        self.assertEqual(result["results"][0]["title"], "Dummy Movie")

    def test_get_movie_details_returns_movie(self):
        movie = self.client.get_movie_details(1)
        self.assertEqual(movie["id"], 1)
        self.assertEqual(movie["title"], "Dummy Movie")
        self.assertEqual(movie["media_type"], "movie")

    def test_get_trending_movies_returns_list(self):
        trending = self.client.get_trending_movies()
        self.assertIn("results", trending)
        self.assertGreater(len(trending["results"]), 0)
        self.assertEqual(trending["results"][0]["title"], "Dummy Movie")

if __name__ == "__main__":
    unittest.main()