from song import Song
import time
import json


class Playlist:

    @staticmethod
    def load(file_name):
        file = open(file_name, "r")
        new_playlist = json.loads(file.read())
        my_playlist = Playlist(new_playlist["name"])
        for song in new_playlist["songs"]:
            my_playlist.add_song(Song(
                song["title"],
                song["artist"],
                song["album"],
                song["length"],
                song["path"]))
        file.close()
        return my_playlist

    def __init__(self, name):
        self.name = name
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def remove_song(self, song):
        self.songs.remove(song)

    def length(self):
        length = 0
        for song in self.songs:
            length += song.length
        return length

    def show_artists(self):
        artists = []
        for song in self.songs:
            artists.append(song.artist)
        return set(artists)

    def __str__(self):
        result = ""
        for song in self.songs:
            format_time = time.strftime("%M:%S", time.gmtime(song.length))
            result += "{} {} - {}".format(song.artist, song.title, format_time)
            result += "\n"
        return result

    def hash_songs(self):
        hashed_songs = []
        for song in self.songs:
            hashed_songs.append(song.hash_song())
        return hashed_songs

    def hash_playlist(self):
        hash_playlist = {}
        hash_playlist["name"] = self.name
        hash_playlist["songs"] = self.hash_songs()
        return hash_playlist

    def save(self, file_name):
        file = open(file_name, "w")
        file.write(json.dumps(self.hash_playlist()))
        file.close()
