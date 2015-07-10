from player.song import Song

import json
import os
from mutagen.mp3 import MP3

from PyQt5.QtCore import QFileInfo, QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent

"""This is a class that wraps together a QMediaPlaylist object -
   the object, needed so that music can be played through QtMultimedia,
   and my representation of a Playlist - a list of Song objects
   and a string for a name. Load and save work with the json format,
   and the files that are saved/loaded are with an extension .ltmp"""


class PlaylistWrapper:
    def __init__(self, name):
        self.name = name
        self.songs = []
        self.playlist = QMediaPlaylist()

    def path_to_song(self, song_path):
        filepath, song_name = os.path.split(song_path)
        os.chdir(filepath)
        audio = MP3(song_name)
        try:
            title = audio["TIT2"]
            artist = audio["TPE1"]
            album = audio["TALB"]
        except KeyError:
            title = artist = album = "Unknown"
        length = audio.info.length
        return Song(title, artist, album, length, song_path)

    def add_song(self, song_path):
        if song_path.split(".")[-1] not in ["mp3", "flac", "ogg"]:
            raise AssertionError
        song = self.path_to_song(song_path)
        filepath = song.path
        fileInfo = QFileInfo(filepath)
        if fileInfo.exists():
            url = QUrl.fromLocalFile(fileInfo.absoluteFilePath())
            if fileInfo.suffix().lower() == "mp3" or "flac" or "ogg":
                self.playlist.addMedia(QMediaContent(url))
                self.songs.append(song)

    def save(self, file_path):
        os.chdir(file_path)
        file = open(self.name + ".ltmp", "w")
        file.write(json.dumps(self.hash_playlist()))
        file.close()

    def load(self, file_path):
        dir_name, file_name = os.path.split(file_path)
        os.chdir(dir_name)
        name_parts = file_name.split(".")

        if not name_parts[-1] == "ltmp":
            raise AssertionError

        with open(file_name, "r") as json_file:
            data = json.load(json_file)
            for song in data["songs"]:
                self.add_song(song["path"])

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

    def is_empty(self):
        return len(self.songs) == 0
