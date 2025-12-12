import unittest
from utils import truncate_text, format_genres, format_rating, format_media_item, format_media_list
from models import MediaItem

class TestFormatters(unittest.TestCase):
    def test_truncate_text_short(self):
        self.assertEqual(truncate_text("Hello", 10), "Hello")

    def test_truncate_text_long(self):
        self.assertEqual(truncate_text("Hello World", 5), "He...")

    def test_format_genres_empty(self):
        self.assertEqual(format_genres([]), "Unknown")

    def test_format_genres_normal(self):
        self.assertEqual(format_genres(["Action", "Comedy"]), "Action, Comedy")

    def test_format_rating_none(self):
        self.assertEqual(format_rating(None), "No rating")

    def test_format_rating_number(self):
        self.assertEqual(format_rating(8.2), "8.2/10")

    def test_format_media_item(self):
        item = MediaItem(id=1, title="My Movie", media_type="movie", genres=["Action"], rating=7.5)
        formatted = format_media_item(item)
        self.assertIn("[movie] My Movie", formatted)
        self.assertIn("Genres: Action", formatted)
        self.assertIn("Rating: 7.5/10", formatted)

    def test_format_media_list_empty(self):
        self.assertEqual(format_media_list([]), "No results found.")

if __name__ == "__main__":
    unittest.main()