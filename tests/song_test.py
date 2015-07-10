import unittest
from player.song import Song


class SongTest(unittest.TestCase):
    def setUp(self):
        self.new_song = Song("Happy",
                             "P.W.",
                             "Happy",
                             200,
                             "/home/evgeniya/Music/happy.mp3")

    def test_init(self):
        self.assertEqual(self.new_song.title, "Happy")
        self.assertEqual(self.new_song.artist, "P.W.")
        self.assertEqual(self.new_song.album, "Happy")
        self.assertEqual(self.new_song.length, 200)
        self.assertEqual(self.new_song.path, "/home/evgeniya/Music/happy.mp3")

    def test_hash_song(self):
        self.assertEqual(self.new_song.hash_song(),
                         {"path": "/home/evgeniya/Music/happy.mp3"})

if __name__ == '__main__':
    unittest.main()
