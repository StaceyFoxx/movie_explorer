from .media_item import MediaItem

class TVShow(MediaItem):
    def __init__(self, id: str, title: str, genres=None, rating=None):
        super().__init__(id, title, "tv", genres, rating)
