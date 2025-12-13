from api.tmdb_client import TMDbClient

from database.repository import (
    init_db_from_schema,
    add_user,
    get_users,
    add_favourite,
    get_favourites_by_user,
    add_history,
    get_history_by_user,
)

from database.models import User, Favourite, HistoryEntry

def prompt_non_empty(message: str) -> str:
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")

def prompt_int(message: str, min_value: int = 1) -> int:
    while True:
        raw = input(message).strip()

        if not raw.isdigit():
            print("Please enter a valid number.")
            continue

        number = int(raw)

        if number < min_value:
            print(f"Number must be at least {min_value}.")
            continue

        return number

def print_banner():
    print("================================")
    print("        Movie Explorer          ")
    print("================================")

def show_menu() -> str:
    print("\nMenu:")
    print("1. Create user")
    print("2. List users")
    print("3. Save a search keyword")
    print("4. Add favourite (manual)")
    print("5. Search TMDb + add favourite")
    print("6. View favourites for a user")
    print("7. View search history for a user")
    print("8. Exit")
    return input("Choose an option (1-8): ").strip()

def create_user():
    print("\n--- Create user ---")
    username = prompt_non_empty("Username: ")
    email = prompt_non_empty("Email: ")

    user = User(id=None, username=username, email=email)
    new_id = add_user(user)
    print(f"User created with ID {new_id}.")

def list_users():
    print("\n--- List users ---")
    users = get_users()
    if not users:
        print("No users found.")
        return

    for u in users:
        print(f"ID {u['id']}: {u['username']} ({u['email']})")

def save_search_keyword():
    print("\n--- Save search keyword ---")
    user_id = prompt_int("User ID: ", min_value=1)
    keyword = prompt_non_empty("Search keyword: ")

    entry = HistoryEntry(id=None, user_id=user_id, search_keyword=keyword)
    add_history(entry)
    print(f"Saved search keyword '{keyword}' for user {user_id}.")

def add_favourite_manual():
    print("\n--- Add favourite (manual) ---")
    user_id = prompt_int("User ID: ", min_value=1)
    movie_id = prompt_non_empty("Movie ID: ")
    title = prompt_non_empty("Movie title: ")
    media_type = input("Media type (movie/tv, blank = movie): ").strip() or "movie"

    fav = Favourite(
        id=None,
        user_id=user_id,
        movie_id=movie_id,
        title=title,
        media_type=media_type,
        genre=None,
        rating=None,
    )
    fav_id = add_favourite(fav)
    print(f"Favourite saved with ID {fav_id}.")

def search_tmdb_and_add_favourite():
    print("\n--- Search TMDb + add favourite ---")
    user_id = prompt_int("User ID: ", min_value=1)
    keyword = prompt_non_empty("Search keyword: ")

    add_history(HistoryEntry(id=None, user_id=user_id, search_keyword=keyword))

    client = TMDbClient()
    results = client.search_multi(keyword)

    if not results:
        print("No results found.")
        return

    print("\nResults:")
    shown = results[:10]
    for i, item in enumerate(shown, start=1):
        title = item.title
        media_type = item.media_type
        print(f"{i}. {title} ({media_type})")

    pick = prompt_int("Choose a number to favourite: ", min_value=1)
    if pick > len(shown):
        print("Invalid choice.")
        return

    chosen = shown[pick - 1]

    fav = Favourite(
        id=None,
        user_id=user_id,
        movie_id=str(chosen.id),
        title=chosen.title,
        media_type=chosen.media_type,
        genre=None,
        rating=None,
    )

    fav_id = add_favourite(fav)
    print(f"Saved '{chosen.title}' as a favourite (ID {fav_id}).")

def view_favourites_for_user():
    print("\n--- View favourites ---")
    user_id = prompt_int("User ID: ", min_value=1)

    favs = get_favourites_by_user(user_id)
    if not favs:
        print("No favourites for this user.")
        return

    print(f"\nFavourites for user {user_id}:")
    for f in favs:
        rating = f["rating"] if f["rating"] is not None else "no rating"
        print(f"ID {f['id']}: {f['title']} ({f['media_type']}, {rating})")

def view_search_history_for_user():
    print("\n--- View search history ---")
    user_id = prompt_int("User ID: ", min_value=1)

    history = get_history_by_user(user_id)
    if not history:
        print("No search history for this user.")
        return

    print(f"\nSearch history for user {user_id}:")
    for h in history:
        print(f"{h['searched_at']}: {h['search_keyword']}")

def main():
    init_db_from_schema()
    print_banner()

    while True:
        choice = show_menu()

        if choice == "1":
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            save_search_keyword()
        elif choice == "4":
            add_favourite_manual()
        elif choice == "5":
            search_tmdb_and_add_favourite()
        elif choice == "6":
            view_favourites_for_user()
        elif choice == "7":
            view_search_history_for_user()
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()