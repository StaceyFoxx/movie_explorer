import unittest
from database.models import User, Favourite, HistoryEntry

class TestUser(unittest.TestCase):

    def test_user_creation(self):
        user = User(id=1, username="alice", email="alice@example.com")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "alice")
        self.assertEqual(user.email, "alice@example.com")
        self.assertIsNone(user.created_at)  # default value

class TestFavourite(unittest.TestCase):

    def test_favourite_creation(self):
        fav = Favourite(
            id=1,
            user_id=1,
            movie_id="m123",
            title="Inception",
            media_type="movie"
        )
        self.assertEqual(fav.id, 1)
        self.assertEqual(fav.user_id, 1)
        self.assertEqual(fav.movie_id, "m123")
        self.assertEqual(fav.title, "Inception")
        self.assertEqual(fav.media_type, "movie")
        self.assertIsNone(fav.genre)      # default
        self.assertIsNone(fav.rating)     # default
        self.assertIsNone(fav.added_at)   # default

class TestHistoryEntry(unittest.TestCase):

    def test_history_entry_creation(self):
        entry = HistoryEntry(
            id=1,
            user_id=1,
            search_keyword="Inception"
        )
        self.assertEqual(entry.id, 1)
        self.assertEqual(entry.user_id, 1)
        self.assertEqual(entry.search_keyword, "Inception")
        self.assertIsNone(entry.searched_at)  # default

if __name__ == "__main__":
    unittest.main()