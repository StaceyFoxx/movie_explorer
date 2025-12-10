class MediaItem:
    def __init__(self, id: str, title: str, media_type: str, genres=None, rating=None):
        self.id = id
        self.title = title
        self.media_type = media_type
        self.genres = genres or []
        self.rating = rating
