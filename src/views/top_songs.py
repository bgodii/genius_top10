import unidecode
from flask_restful import Resource, inputs, reqparse

from helpers.helpers import Helpers
from services import dynamo_db, genius_api, redis_instance


class TopSongs(Resource):
    genius_api = genius_api.GeniusApi()
    dynamo_db = dynamo_db.DynamoDb("artists")
    redis = redis_instance.Redis()

    parser = reqparse.RequestParser()
    parser.add_argument("cache", type=inputs.boolean, default=True)
    parser.add_argument("artist", type=str, required=True)

    def get(self):
        request_data = self.parser.parse_args()
        artist = unidecode.unidecode(
            request_data["artist"]
        ).lower()  # remove accents and transform to lowercase

        cache = request_data["cache"]
        artist_data = self.dynamo_db.get("artist_name", artist)

        if cache and artist_data:
            cache_data = self.redis.get_list(artist_data["transaction_id"])
            songs_sorted = Helpers.create_enumerate_song_list(cache_data)

            return {"artist": artist, "top_songs": songs_sorted}, 200

        response = self.genius_api.get_top_songs(artist)

        if not response:
            return {"message": "not resource"}, 404
        elif response.get("meta", {}):
            response = response["meta"]
            return {"message": response["message"]}, response["status"]

        songs = response["message"]

        transaction_id = self.dynamo_db.create(
            key_name="artist_name", key_value=artist, songs=songs
        )

        transaction_id = {
            "new": transaction_id,
            "old": artist_data.get("transaction_id"),
        }

        self.redis.manage_lists(transaction_id, songs)
        songs_sorted = Helpers.create_enumerate_song_list(songs)

        return {"artist": artist, "top_songs": songs_sorted}, 200
