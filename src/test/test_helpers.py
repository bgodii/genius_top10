from unittest import TestCase
from unittest.mock import MagicMock
from helpers.helpers import Helpers


class TestHelpers(TestCase):
    def test_create_enumerate_song_dict(self):
        songs = ["test_song0", "test_song1", "test_song2"]
        enumerate_songs = {1: songs[0], 2: songs[1], 3: songs[2]}
        response = Helpers.create_enumerate_song_list(songs)

        self.assertEqual(response, enumerate_songs)

    def test_decode_list(self):
        songs = ["test_song0", "test_song1", "test_song2"]
        encoded_songs = [song.encode("utf-8") for song in songs]

        response = Helpers.decode_list(encoded_songs)

        self.assertEqual(response, songs)
