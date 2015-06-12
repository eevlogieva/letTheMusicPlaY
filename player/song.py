class Song():
    def __init__(self, title, artist, album, length, filepath):
        self.title = title
        self.artist = artist
        self.album = album
        self.rating = 3
        self.length = length
        self.filepath = filepath

    def hash_song(self):
        hashed_song = {}
        hashed_song["title"] = self.title
        hashed_song["artist"] = self.artist
        hashed_song["album"] = self.album
        hashed_song["length"] = self.length
        hashed_song["rating"] = self.rating
        return hashed_song
