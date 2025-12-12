class TMDbClient:
    def search_movie(self, keyword):
        # Returns dummy search result
        return {"results": [{"id": 1, "title": "Dummy Movie", "media_type": "movie"}]}

    def get_movie_details(self, movie_id):
        # Returns dummy movie details
        return {"id": movie_id, "title": "Dummy Movie", "media_type": "movie"}

    def get_trending_movies(self):
        # Returns dummy trending list
        return {"results": [{"id": 1, "title": "Dummy Movie", "media_type": "movie"}]}