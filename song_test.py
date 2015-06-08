import unittest
from song import Song


class SongTest(unittest.TestCase):
    def setUp(self):
        self.new_song = Song("Happy",
                             "P.W.",
                             "Happy",
                             200,
                             64)

    def test_init(self):
        self.assertEqual(self.new_song.title, "Happy")
        self.assertEqual(self.new_song.artist, "P.W.")
        self.assertEqual(self.new_song.album, "Happy")
        self.assertFalse(self.new_song.rating)
        self.assertEqual(self.new_song.length, 200)
        self.assertEqual(self.new_song.bitrate, 64)

    def test_rate_function_in_range(self):
        self.new_song.rate(4)
        self.assertEqual(self.new_song.rating, 4)

    def test_rate_function_out_of_range(self):
        with self.assertRaises(ValueError):
            self.new_song.rate(6)


if __name__ == '__main__':
    unittest.main()
