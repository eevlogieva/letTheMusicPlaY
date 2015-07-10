import glob
import os


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
