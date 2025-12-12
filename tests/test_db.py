import unittest
from unittest import mock
from database import db_connection, config

class TestDBConnection(unittest.TestCase):

    def setUp(self):
        # Patch DB_PATH to use in-memory database for isolation
        self.patcher = mock.patch.object(config, "DB_PATH", ":memory:")
        self.patcher.start()

        # Create table in memory
        conn = db_connection.get_connection()
        conn.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT);")
        conn.commit()
        conn.close()

    def tearDown(self):
        # Stop patching DB_PATH
        self.patcher.stop()

    def test_basic_db_operations(self):
        # Test connection
        conn = db_connection.get_connection()
        self.assertIsNotNone(conn)
        self.assertEqual(conn.row_factory.__name__, "Row")
        conn.close()

        # Test insert
        movie_id = db_connection.execute_query(
            "INSERT INTO movies (title) VALUES (?);",
            ("Inception",)
        )
        self.assertEqual(movie_id, 1)

        # Test fetch
        rows = db_connection.fetch_query("SELECT * FROM movies;")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "Inception")

        # Test fetch with no data
        db_connection.execute_query("DELETE FROM movies;")
        rows = db_connection.fetch_query("SELECT * FROM movies;")
        self.assertEqual(rows, [])


if __name__ == "__main__":
    unittest.main()