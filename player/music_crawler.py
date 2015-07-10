import glob
import os

"""Given an object of PlaylistWrapper, crawler's generate_playlist
   crawls its folder and tries to add everything in the wrapper.
   In the wrapper's add_song, there are validations of the
   path that is given, so it would work properly."""


class MusicCrawler:
    def __init__(self, file_path_to_crawl):
        self.path = file_path_to_crawl

    def generate_playlist(self, wrapper):
        os.chdir(self.path)
        for filename in glob.glob("*"):
            filepath = os.path.join(self.path, filename)
            try:
                wrapper.add_song(filepath)
            except AssertionError:
                pass
