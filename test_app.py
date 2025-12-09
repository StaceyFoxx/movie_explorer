# test_app.py
from pathlib import Path

from database import (
    init_db_from_schema,
    User,
    Favourite,
    HistoryEntry,
    add_user,
    get_users,
    get_user_by_email,
    add_favourite,
    get_favourites_by_user,
    delete_favourite,
    find_favourite,
    add_history,
    get_history_by_user,
    clear_history_by_user,
)
from database.config import DB_PATH


def main():
    print("Using DB:", DB_PATH)

    # 1) Init DB from schema (schema.sql is at project root)
    schema_path = Path(__file__).parent / "database" / "schema.sql"
    init_db_from_schema(str(schema_path))
    print("DB initialized from schema")

    # 2) Create a user
    user = User(id=None, username="test_user", email="test@example.com", created_at=None)
    user_id = add_user(user)
    print("Inserted user id:", user_id)

    # 3) Fetch users and by email
    users = get_users()
    print("All users:", users)

    fetched = get_user_by_email("test@example.com")
    print("User by email:", fetched)

    # 4) Add a favourite
    fav = Favourite(
        id=None,
        user_id=user_id,
        movie_id="tt1234567",
        title="Test Movie",
        media_type="movie",
        genre="Drama",
        rating=4.5,
        added_at=None,
    )
    fav_id = add_favourite(fav)
    print("Inserted favourite id:", fav_id)

    # 5) Get favourites and find/delete one
    favs = get_favourites_by_user(user_id)
    print("Favourites for user:", favs)

    found = find_favourite(user_id, "tt1234567")
    print("Found favourite:", found)

    delete_favourite(fav_id)
    print("Deleted favourite id:", fav_id)

    favs_after = get_favourites_by_user(user_id)
    print("Favourites after delete:", favs_after)

    # 6) History operations
    h1 = HistoryEntry(
        id=None,
        user_id=user_id,
        search_keyword="test search",
        searched_at=None,
    )
    h_id = add_history(h1)
    print("Inserted history id:", h_id)

    history = get_history_by_user(user_id)
    print("History for user:", history)

    clear_history_by_user(user_id)
    print("Cleared history")

    history_after = get_history_by_user(user_id)
    print("History after clear:", history_after)


if __name__ == "__main__":
    main()
