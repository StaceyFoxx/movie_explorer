"""
Generic helper functions for console I/O and input validation.
"""

from typing import Callable, Iterable, TypeVar, Optional

T = TypeVar("T")


def print_divider(char: str = "-", length: int = 50) -> None:
    """
    Print a horizontal divider line.
    """
    print(char * length)


def clear_screen() -> None:
    """
    Clear the terminal screen in a cross‑platform way.
    """
    import os
    import platform

    command = "cls" if platform.system().lower().startswith("win") else "clear"
    os.system(command)


def pause(message: str = "Press Enter to continue...") -> None:
    """
    Simple pause, waits for the user to press Enter.
    """
    input(message)


def prompt_non_empty(prompt_text: str) -> str:
    """
    Ask the user for input until they enter a non‑empty string.
    """
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def prompt_int(
    prompt_text: str,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
) -> int:
    """
    Ask the user for an integer, optionally enforcing a min/max range.
    """
    while True:
        raw = input(prompt_text).strip()
        if not raw:
            print("Please enter a number.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("Invalid number, please try again.")
            continue

        if min_value is not None and value < min_value:
            print(f"Value must be at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Value must be at most {max_value}.")
            continue
        return value


def choose_from_list(
    items: Iterable[T],
    item_to_str: Callable[[T], str] = str,
    allow_cancel: bool = True,
) -> Optional[T]:
    """
    Let the user pick one item from a list.

    Returns the selected item, or None if the user cancels.
    """
    items = list(items)
    if not items:
        print("Nothing to choose from.")
        return None

    # Show menu
    for idx, item in enumerate(items, start=1):
        print(f"{idx}. {item_to_str(item)}")

    if allow_cancel:
        print("0. Cancel")

    while True:
        choice = prompt_int("Choose an option: ", min_value=0, max_value=len(items))
        if choice == 0 and allow_cancel:
            return None
        if 1 <= choice <= len(items):
            return items[choice - 1]
