# Movie Explorer

## Summary
This project is part of a CFG group assignment. It is designed for people who struggle to remember movies or feel lost among too many options. The app provides a quick and easy way to search movies and TV shows, view details, and see trending titles, helping users make decisions faster.

## Overview
A console-based Python app to search movies and TV shows using the TMDb API. Users can view movie details, trending movies, and more.

## Team Responsibilities

 - Database & ORM (SQLite) – Laila: db/

- API Module (TMDb) – Stacey: tmdb_client.py

- Core Logic Module – Khadija: models/ + services/

- Main & Run Script – Zara: main.py

- Utils Module – Nada: utils/

- Tests – Ayesha: tests/

## Setup
1. Clone the repository.
2. Install dependencies:

```
bash
pip install requests python-dotenv
````

3. Create a ```.env``` file in the project root with your TMDb API key:

```
TMDB_API_KEY = your_api_key_here
````

4. Run the app:

```
python main.py
````



_Notes_

- ```.env``` is ignored in Git to keep the API key private.

- SQLite database files (*.db) can be regenerated from db/schema.sql.

- Use Python 3.9+ for best compatibility.