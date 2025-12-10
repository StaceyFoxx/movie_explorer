from .media_item import MediaItem

class Movie(MediaItem):
    def __init__(self, id: str, title: str, genres=None, rating=None):
        super().__init__(id, title, "movie", genres, rating)
