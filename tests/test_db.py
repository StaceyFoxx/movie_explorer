import unittest
import tempfile
import os
from unittest import mock
from database import db_connection, config


class TestDBConnection(unittest.TestCase):
    """
    Tests basic database connection and query functionality.

    Temporary database is used so the real database
    isn't affected during testing.
    """

    def setUp(self):
        """
        Creates a temporary database before each test.

        This runs before every test method and allows us to work with a clean database.
        """
        # creates temporary database file for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()

        # points app to temporary database
        self.patcher = mock.patch.object(config, "DB_PATH", self.temp_db.name)
        self.patcher.start()

        # creates table for testing database operations
        conn = db_connection.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY,
                title TEXT
            );
        """)
        conn.commit()
        conn.close()

    def tearDown(self):
        """
        Removes the temporary database and
        resets any mocked values after each test.
        """
        # stops mocking database path
        self.patcher.stop()

        # deletes the temporary database
        os.unlink(self.temp_db.name)

    def test_basic_db_operations(self):
        """
        Test basic database behaviour.

        This includes:
        - opening a connection
        - inserting data
        - fetching data
        - handling empty results
        """

        # checks database connection can be created
        conn = db_connection.get_connection()
        self.assertIsNotNone(conn)

        # ensures rows are returned as dictionary-like objects
        self.assertEqual(conn.row_factory.__name__, "Row")
        conn.close()

        # inserts a movie into database (e.g. Inception)
        movie_id = db_connection.execute_query(
            "INSERT INTO movies (title) VALUES (?);",
            ("Inception",)
        )

        # first inserted row should have ID of 1
        self.assertEqual(movie_id, 1)

        # fetches all movies from database
        rows = db_connection.fetch_query("SELECT * FROM movies;")

        # checks if movie was saved correctly
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "Inception")

        # deletes all movies and checks if the table is empty
        db_connection.execute_query("DELETE FROM movies;")
        rows = db_connection.fetch_query("SELECT * FROM movies;")

        self.assertEqual(rows, [])