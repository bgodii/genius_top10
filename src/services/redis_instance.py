from datetime import timedelta

import redis
from helpers.helpers import Helpers


class Redis:
    redis = redis.Redis(host="redis", port=6379, db=0)

    def manage_lists(self, key, args, expiration_time=timedelta(days=7)):
        if key.get("old"):
            self.redis.delete(key["old"])

        self.redis.rpush(key.get("new"), *args)
        self.redis.expire(key.get("new"), expiration_time)

    def get_list(self, key, start=0, end=-1):
        encoded_list = self.redis.lrange(key, start, end)
        return Helpers.decode_list(encoded_list)
