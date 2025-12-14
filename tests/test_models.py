import unittest
from database.models import User, Favourite, HistoryEntry


class TestUser(unittest.TestCase):
    """
    Tests User model.

    Checks if User object stores the right values
    and default fields are handled correctly.
    """

    def test_user_creation(self):
        """
        Tests creating a user using name and email.
        """
        # create User object
        user = User(id=1, username="Ayesha", email="ayesha1996@example.com")

        # check all fields are saved correctly
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "Ayesha")
        self.assertEqual(user.email, "ayesha1996@example.com")

        # created_at should default to None
        self.assertIsNone(user.created_at)


class TestFavourite(unittest.TestCase):
    """
    Tests Favourite model.

    Checks favourite movies are stored correctly
    and optional fields default to None.
    """

    def test_favourite_creation(self):
        """
        Tests creating a favourite movie.
        """
        # creates Favourite object
        fav = Favourite(
            id=1,
            user_id=1,
            movie_id="m123",
            title="Inception",
            media_type="movie"
        )

        # checks required fields
        self.assertEqual(fav.id, 1)
        self.assertEqual(fav.user_id, 1)
        self.assertEqual(fav.movie_id, "m123")
        self.assertEqual(fav.title, "Inception")
        self.assertEqual(fav.media_type, "movie")

        # optional fields should be None
        self.assertIsNone(fav.genre)
        self.assertIsNone(fav.rating)
        self.assertIsNone(fav.added_at)


class TestHistoryEntry(unittest.TestCase):
    """
    Tests HistoryEntry model.

    Ensures search history entries are created correctly.
    """

    def test_history_entry_creation(self):
        """
        Tests creating a history entry.
        """
        # creates HistoryEntry object
        entry = HistoryEntry(
            id=1,
            user_id=1,
            search_keyword="Inception"
        )

        # checks fields are stored correctly
        self.assertEqual(entry.id, 1)
        self.assertEqual(entry.user_id, 1)
        self.assertEqual(entry.search_keyword, "Inception")

        # searched_at should default to None
        self.assertIsNone(entry.searched_at)


if __name__ == "__main__":
    unittest.main()