import os

import requests


class GeniusApi:
    SEARCH_URL = "https://api.genius.com/search?q={}&text_format=plain"
    AUTH_TOKEN = os.environ.get("AUTH_TOKEN", None)

    def get_top_songs(self, artist_name) -> list:
        url = self.SEARCH_URL.format(artist_name)
        headers = {"Authorization": "Bearer {}".format(self.AUTH_TOKEN)}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response = response.json()

            top_songs = self._extract_top_songs(response["response"])

            return {"message": top_songs, "status": 200}

        except requests.exceptions.HTTPError as err:
            return err.response.json()

    def _extract_top_songs(self, response) -> list:
        hits = response.get("hits", None)
        song_names = [hit.get("result", {}).get("title") for hit in hits]
        return song_names
