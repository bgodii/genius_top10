from datetime import timedelta
from unittest import TestCase
from unittest.mock import MagicMock

from helpers.helpers import Helpers
from services.redis_instance import Redis


class TestRedis(TestCase):
    def setUp(self) -> None:
        self.redis = Redis()
        self.helper = Helpers()

    def test_manage_lists(self):
        songs = ["test_song0", "test_song1", "test_song2"]
        keys = {
            "old": "some_old_transaction_id",
            "new": "some_new_transaction__id",
        }

        self.redis.redis_instance.delete = MagicMock()
        self.redis.redis_instance.rpush = MagicMock()
        self.redis.redis_instance.expire = MagicMock()

        self.redis.manage_lists(keys, songs)

        self.redis.redis_instance.delete.assert_called_once_with(keys["old"])
        self.redis.redis_instance.rpush.assert_called_once_with(
            keys["new"], *songs
        )
        self.redis.redis_instance.expire.assert_called_once_with(
            keys["new"], timedelta(days=7)
        )

    def test_get_list(self):
        songs = [u"test_song0", u"test_song1", u"test_song2"]

        self.redis.redis_instance.lrange = MagicMock(return_value=songs)
        Helpers.decode_list = MagicMock()

        self.redis.get_list("some_transaction_id")

        self.redis.redis_instance.lrange.assert_called_once_with(
            "some_transaction_id", 0, -1
        )
        Helpers.decode_list.assert_called_once_with(songs)
