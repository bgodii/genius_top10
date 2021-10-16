from datetime import timedelta

import redis
from helpers.helpers import Helpers


class Redis:
    redis = redis.Redis(host="redis", port=6379, db=0)

    def manage_lists(self, key, args, expiration_time=timedelta(days=7)):
        key_exist = self.redis.get(key)

        if key_exist:
            self.redis.delete(key)

        self.redis.rpush(key, *args)
        self.redis.expire(key, expiration_time)

    def get_list(self, key, start=0, end=-1):
        encoded_list = self.redis.lrange(key, start, end)
        return Helpers.decode_list(encoded_list)
