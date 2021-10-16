from flask_restful import Resource, reqparse

from services.genius_api import GeniusApi


class TopSongs(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("cache", type=bool, default=True)
    parser.add_argument("artist", type=str, required=True)

    def get(self):
        genius_api = GeniusApi()
        request_data = self.parser.parse_args()
        artist = request_data["artist"]
        response = genius_api.get_top_songs(artist)

        if not response:
            return {"message": "not resource"}, 404
        elif response.get("meta", {}):
            response = response["meta"]
            return {"message": response["message"]}, response["status"]

        songs = response["message"]
        top_songs = {idx + 1: value for (idx, value) in enumerate(songs)}

        return {"artist": artist, "top_songs": top_songs}, 200
