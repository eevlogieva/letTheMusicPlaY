from player.playlist_wrapper import PlaylistWrapper
from player.song import Song
import unittest
import os


class PlaylistWrapperTest(unittest.TestCase):
    def setUp(self):
        self.new_playlist = PlaylistWrapper("testSongs")
        self.song_one = Song("One", "Ed Sheeran", "x", 252,
                             "/home/evgeniya/Music/Ed/One.mp3")
        self.song_two = Song("Sing", "Ed Sheeran", "x", 235,
                             "/home/evgeniya/Music/Ed/Sing.mp3")

    def test_init(self):
        self.assertEqual(self.new_playlist.name, "testSongs")

    def test_add_song_valid_song(self):
        self.new_playlist.add_song(self.song_one.path)
        self.assertEqual(self.new_playlist.songs[0].title, self.song_one.title)

    def test_add_song_invalid_path(self):
        with self.assertRaises(AssertionError):
            self.new_playlist.add_song("/home/a.txt")

    def test_save_load(self):
        self.new_playlist.add_song(self.song_one.path)
        self.new_playlist.add_song(self.song_two.path)
        self.new_playlist.save("/home/evgeniya/Music")
        my_playlist = PlaylistWrapper("test")
        self.test_location = "/home/evgeniya/Music/testSongs.ltmp"
        my_playlist.load(self.test_location)
        self.assertEqual(my_playlist.songs[0].title, self.song_one.title)
        self.assertEqual(my_playlist.songs[1].title, self.song_two.title)

        os.remove(self.test_location)

    def test_load_from_invalid_path(self):
        with self.assertRaises(AssertionError):
            self.new_playlist.load("/home/evgeniya/Music/a.txt")

    def test_path_to_song(self):
        new = self.new_playlist.path_to_song("/home/evgeniya/Music/Ed/One.mp3")
        self.assertEqual(new.title, self.song_one.title)

    def test_is_empty_empty(self):
        self.assertTrue(self.new_playlist.is_empty())

    def test_is_empty_not_empty(self):
        self.new_playlist.add_song(self.song_one.path)
        self.assertFalse(self.new_playlist.is_empty())

    def test_hash_songs(self):
        self.new_playlist.add_song(self.song_one.path)
        self.new_playlist.add_song(self.song_two.path)
        self.assertEqual(self.new_playlist.hash_songs(),
                         [{"path": "/home/evgeniya/Music/Ed/One.mp3"},
                          {"path": "/home/evgeniya/Music/Ed/Sing.mp3"}])

    def test_hash_playlist(self):
        self.new_playlist.add_song(self.song_one.path)
        self.new_playlist.add_song(self.song_two.path)
        self.assertEqual(
            self.new_playlist.hash_playlist(),
            {"name": "testSongs",
             "songs": [{"path": "/home/evgeniya/Music/Ed/One.mp3"},
                       {"path": "/home/evgeniya/Music/Ed/Sing.mp3"}]}
        )


if __name__ == '__main__':
    unittest.main()
