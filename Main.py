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


def print_banner():
    print("================================")
    print("        Movie Explorer          ")
    print("================================")


def show_menu():
    print("\nMenu:")
    print("1. Create user")
    print("2. List users")
    print("3. Save a search keyword")
    print("4. Add favourite (manual)")
    print("5. View favourites for a user")
    print("6. View search history for a user")
    print("7. Exit")
    return input("Choose an option (1-7): ").strip()


def main():
    init_db_from_schema()
    print_banner()

    while True:
        choice = show_menu()

        if choice == "1":
            username = input("Username: ").strip()
            email = input("Email: ").strip()

            if username == "" or email == "":
                print("Username and email cannot be empty.")
                continue

            user = User(id=None, username=username, email=email)
            new_id = add_user(user)
            print(f"User created with ID {new_id}.")

        elif choice == "2":
            users = get_users()
            if not users:
                print("No users found.")
            else:
                print("\nUsers:")
                for u in users:
                    print(f"ID {u['id']}: {u['username']} ({u['email']})")

        elif choice == "3":
            user_id_text = input("User ID: ").strip()
            if not user_id_text.isdigit():
                print("User ID must be a number.")
                continue
            user_id = int(user_id_text)

            keyword = input("Search keyword: ").strip()
            if keyword == "":
                print("Search keyword cannot be empty.")
                continue

            entry = HistoryEntry(id=None, user_id=user_id, search_keyword=keyword)
            add_history(entry)
            print(f"Saved search keyword '{keyword}' for user {user_id}.")

        elif choice == "4":
            # Add favourite manually
            user_id_text = input("User ID: ").strip()
            if not user_id_text.isdigit():
                print("User ID must be a number.")
                continue
            user_id = int(user_id_text)

            movie_id = input("Movie ID: ").strip()
            title = input("Movie title: ").strip()
            media_type = input("Media type (movie/tv, blank = movie): ").strip()
            if media_type == "":
                media_type = "movie"

            if movie_id == "" or title == "":
                print("Movie ID and title cannot be empty.")
                continue

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

        elif choice == "5":
            user_id_text = input("User ID: ").strip()
            if not user_id_text.isdigit():
                print("User ID must be a number.")
                continue
            user_id = int(user_id_text)

            favs = get_favourites_by_user(user_id)
            if not favs:
                print("No favourites for this user.")
            else:
                print("\nFavourites:")
                for f in favs:
                    rating = f["rating"] if f["rating"] is not None else "no rating"
                    print(f"ID {f['id']}: {f['title']} ({f['media_type']}, {rating})")

        elif choice == "6":
            user_id_text = input("User ID: ").strip()
            if not user_id_text.isdigit():
                print("User ID must be a number.")
                continue
            user_id = int(user_id_text)

            history = get_history_by_user(user_id)
            if not history:
                print("No search history for this user.")
            else:
                print("\nSearch history:")
                for h in history:
                    print(f"{h['searched_at']}: {h['search_keyword']}")

        elif choice == "7":
            print("Goodbye.")
            break

        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()


