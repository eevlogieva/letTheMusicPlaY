from mutagen.mp3 import MP3
from playlist import Playlist
from song import Song
import glob
import os


class MusicCrawler:
    def __init__(self, file_path):
        self.path = file_path

    def generate_playlist(self, name):
        os.chdir(self.path)
        new_playlist = Playlist(name)
        for file in glob.glob("*.mp3"):
            audio = MP3(file)
            new_playlist.add_song(Song(audio["TIT2"],
                                       audio["TPE1"],
                                       audio["TALB"],
                                       audio.info.length,
                                       self.path + '/' + file))
        return new_playlist
