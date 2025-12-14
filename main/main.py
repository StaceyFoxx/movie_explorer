import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(PROJECT_ROOT)

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

def pause():
    input("\nPress Enter to return to the menu...")

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
    print("3. Add favourite (manual)")
    print("4. Search movies")
    print("5. View favourites for a user")
    print("6. View search history for a user")
    print("7. Exit")
    return input("Choose an option (1-7): ").strip()

def create_user():
    print("\n--- Create user ---")
    username = prompt_non_empty("Username: ")
    email = prompt_non_empty("Email: ")

    user = User(id=None, username=username, email=email)
    new_id = add_user(user)
    print(f"\nUser created with ID {new_id}.")
    pause()

def list_users():
    print("\n--- List users ---")
    users = get_users()

    if not users:
        print("No users found.")
    else:
        for u in users:
            print(f"ID {u['id']}: {u['username']} ({u['email']})")

    pause()

def add_favourite_manual():
    print("\n--- Add favourite (manual) ---")
    user_id = prompt_int("User ID: ")
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
    print(f"\nFavourite saved with ID {fav_id}.")
    pause()

def search_movies():
    print("\n--- Search movies ---")
    user_id = prompt_int("User ID: ")
    keyword = prompt_non_empty("What movie do you want to search for? ")

    add_history(HistoryEntry(id=None, user_id=user_id, search_keyword=keyword))

    try:
        client = TMDbClient()
    except ValueError as e:
        print(str(e))
        print("Check your .env file is in the project root and contains TMDB_API_KEY=...")
        pause()
        return

    data = client.search_movie(keyword)

    if not data or "results" not in data or not data["results"]:
        print("No results found.")
        pause()
        return

    results = data["results"][:10]

    print("\nResults:")
    for i, item in enumerate(results, start=1):
        title = item.get("title", "Unknown title")
        release_date = item.get("release_date", "")
        year = release_date[:4] if release_date else ""
        year_text = f" ({year})" if year else ""
        print(f"{i}. {title}{year_text}")

    pause()

def view_favourites_for_user():
    print("\n--- View favourites ---")
    user_id = prompt_int("User ID: ")

    favs = get_favourites_by_user(user_id)
    if not favs:
        print("No favourites for this user.")
    else:
        for f in favs:
            rating = f["rating"] if f["rating"] is not None else "no rating"
            print(f"ID {f['id']}: {f['title']} ({f['media_type']}, {rating})")

    pause()

def view_search_history_for_user():
    print("\n--- View search history ---")
    user_id = prompt_int("User ID: ")

    history = get_history_by_user(user_id)
    if not history:
        print("No search history for this user.")
    else:
        for h in history:
            print(f"{h['searched_at']}: {h['search_keyword']}")

    pause()

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
            add_favourite_manual()
        elif choice == "4":
            search_movies()
        elif choice == "5":
            view_favourites_for_user()
        elif choice == "6":
            view_search_history_for_user()
        elif choice == "7":
            print("\nGoodbye 👋")
            break
        else:
            print("Invalid option, try again.")
            pause()

if __name__ == "__main__":
    main()
