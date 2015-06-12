from playlist import Playlist
from song import Song
import unittest


class PlaylistTest(unittest.TestCase):
    def setUp(self):
        self.new_playlist = Playlist("AC/DC Songs")
        self.new_song = Song(
            "Happy",
            "P.W",
            "Happy",
            200,
            128)
        self.song_two = Song("Me", "You", "aaa", 300, 32)

    def test_init(self):
        self.assertEqual(self.new_playlist.name, "AC/DC Songs")

    def test_add_song(self):
        self.new_playlist.add_song(self.new_song)
        self.assertEqual(self.new_playlist.songs[0], self.new_song)

    def test_remove_song(self):
        self.new_playlist.add_song(self.new_song)
        self.new_playlist.remove_song("Happy")
        self.assertFalse(self.new_playlist.songs)

    def test_length(self):
        self.new_playlist.add_song(self.new_song)
        self.new_playlist.add_song(self.song_two)
        self.assertEqual(self.new_playlist.length(), 500)

    def test_remove_disrated(self):
        self.new_song.rate(2)
        self.new_playlist.add_song(self.new_song)
        self.song_two.rate(4)
        self.new_playlist.add_song(self.song_two)
        self.new_playlist.remove_disrated(3)
        self.assertEqual(self.new_playlist.songs, [self.song_two])

    def test_remove_bad_quality(self):
        self.new_playlist.add_song(self.new_song)
        self.new_playlist.add_song(self.song_two)
        self.new_playlist.remove_bad_quality()
        self.assertEqual(self.new_playlist.songs, [self.new_song])

    def test_show_artists(self):
        self.new_playlist.add_song(self.new_song)
        self.new_playlist.add_song(self.song_two)
        self.assertEqual(self.new_playlist.show_artists(), {"P.W", "You"})

    def test_str(self):
        self.new_playlist.add_song(self.new_song)
        self.new_playlist.add_song(self.song_two)
        self.assertEqual(self.new_playlist.__str__(), "P.W Happy - 03:20" + "\n" + "You Me - 05:00" + "\n")

    def test_save_load(self):
        self.new_playlist.add_song(self.new_song)
        self.new_playlist.add_song(self.song_two)
        self.new_playlist.save("test1.json")
        my_playlist = Playlist.load("test1.json")
        self.assertEqual(my_playlist.songs[0].title, self.new_song.title)
        self.assertEqual(my_playlist.songs[1].title, self.song_two.title)

if __name__ == '__main__':
    unittest.main()
