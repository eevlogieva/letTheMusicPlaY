class Song():
    def __init__(self, title, artist, album, length, path):
        self.title = title
        self.artist = artist
        self.album = album
        self.length = length
        self.path = path

    def hash_song(self):
        hashed_song = {}
        hashed_song["path"] = self.path
        return hashed_song
