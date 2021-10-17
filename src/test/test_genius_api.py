from test.mock import genius_api as mock_genius_api
from unittest import TestCase
from unittest.mock import MagicMock

import requests

from services.genius_api import GeniusApi


class TestGeniusApi(TestCase):
    def setUp(self) -> None:
        self.genius_api = GeniusApi()
        self.artist_name = "artist_name_test"
        self.mock_response = requests.Response
        self.mock_response.status_code = 200

    def test_extract_top_songs(self):
        api_response = self.genius_api._extract_top_songs(
            mock_genius_api.response["response"]
        )
        self.assertEqual(api_response, ["title_test", "title_test1"])

    def test_success_return(self):
        self.mock_response.raise_for_status = MagicMock()
        self.mock_response.json = MagicMock(
            return_value=mock_genius_api.response
        )

        requests.get = MagicMock(return_value=self.mock_response)

        api_response = self.genius_api.get_top_songs(self.artist_name)

        self.assertEqual(api_response["status"], 200)
        self.assertEqual(
            api_response["message"], ["title_test", "title_test1"]
        )
