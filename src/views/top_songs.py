import unidecode
from flask_restful import Resource, reqparse

from services import dynamo_db, genius_api


class TopSongs(Resource):
    genius_api = genius_api.GeniusApi()
    dynamo_db = dynamo_db.DynamoDb("artists")

    parser = reqparse.RequestParser()
    parser.add_argument("cache", type=bool, default=True)
    parser.add_argument("artist", type=str, required=True)

    def get(self):
        request_data = self.parser.parse_args()
        artist = unidecode.unidecode(
            request_data["artist"]
        ).lower()  # remove accents and transform to lowercase
        cache = request_data["cache"]

        artist_data = self.dynamo_db.get("artist_name", artist)

        if cache and artist_data:
            return {"artist": artist, "top_songs": artist_data["songs"]}, 200

        response = self.genius_api.get_top_songs(artist)

        if not response:
            return {"message": "not resource"}, 404
        elif response.get("meta", {}):
            response = response["meta"]
            return {"message": response["message"]}, response["status"]

        songs = response["message"]

        self.dynamo_db.create(
            key_name="artist_name", key_value=artist, songs=songs
        )

        top_songs = {idx + 1: value for (idx, value) in enumerate(songs)}

        return {"artist": artist, "top_songs": top_songs}, 200
