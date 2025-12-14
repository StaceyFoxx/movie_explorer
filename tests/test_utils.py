import unittest
from utils import truncate_text, format_genres, format_rating, format_media_item, format_media_list
from models import MediaItem


class TestFormatters(unittest.TestCase):
    """
    Tests utility formatting functions for text, genres, ratings, and media items.

    Ensures output is correct for short/long text, empty/non-empty genres,
    rating formats, and lists of media items.
    """

    def test_truncate_text_short(self):
        """
        Tests truncate_text on short string that doesn't need truncation.
        """
        # short text should remain unchanged
        self.assertEqual(truncate_text("Avatar", 10), "Avatar")

    def test_truncate_text_long(self):
        """
        Tests truncate_text on long string that needs truncation.
        """
        # text longer than max length should be shortened with "..."
        self.assertEqual(truncate_text("Avengers: Endgame", 8), "Aveng...")

    def test_format_genres_empty(self):
        """
        Tests format_genres when no genres are provided.
        """
        # empty genre list should return "Unknown"
        self.assertEqual(format_genres([]), "Unknown")

    def test_format_genres_normal(self):
        """
        Tests format_genres with multiple genres.
        """
        # multiple genres should be joined with comma
        self.assertEqual(format_genres(["Action", "Sci-Fi"]), "Action, Sci-Fi")

    def test_format_rating_none(self):
        """
        Tests format_rating when rating is None.
        """
        # None rating should return "No rating"
        self.assertEqual(format_rating(None), "No rating")

    def test_format_rating_number(self):
        """
        Tests format_rating when rating is a number.
        """
        # numeric rating should be formatted with /10
        self.assertEqual(format_rating(9.1), "9.1/10")

    def test_format_movie_item(self):
        """
        Tests format_media_item for a movie.
        """
        # creates example movie item
        movie = MediaItem(
            id=1,
            title="Inception",
            media_type="movie",
            genres=["Action", "Thriller"],
            rating=8.8
        )

        # formats movie
        formatted = format_media_item(movie)

        # checks formatted String includes all expected parts
        self.assertIn("[movie] Inception", formatted)
        self.assertIn("Genres: Action, Thriller", formatted)
        self.assertIn("Rating: 8.8/10", formatted)

    def test_format_tv_show_item(self):
        """
        Tests format_media_item for a TV show.
        """
        # creates example TV show item
        tv_show = MediaItem(
            id=2,
            title="Stranger Things",
            media_type="tv_show",
            genres=["Drama", "Fantasy"],
            rating=8.7
        )

        # formats TV show
        formatted = format_media_item(tv_show)

        # checks formatted String includes all expected parts
        self.assertIn("[tv_show] Stranger Things", formatted)
        self.assertIn("Genres: Drama, Fantasy", formatted)
        self.assertIn("Rating: 8.7/10", formatted)

    def test_format_media_list_empty(self):
        """
        Tests format_media_list with empty list.
        """
        # empty media list should return "No results found."
        self.assertEqual(format_media_list([]), "No results found.")


if __name__ == "__main__":
    unittest.main()