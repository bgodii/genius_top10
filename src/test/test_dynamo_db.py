from test.mock import dynamo_db as mock_dynamo_db
from unittest import TestCase
from unittest.mock import MagicMock

from services.dynamo_db import DynamoDb


class TestDynamoDb(TestCase):
    def setUp(self) -> None:
        self.dynamo_db = DynamoDb(table_name="teste")
        self.dynamo_db.client = MagicMock()
        self.dynamo_db.dynamo_db = MagicMock()
        self.dynamo_db_sdk = self.dynamo_db.dynamo_db

        self.key = "artist_name"
        self.value = "some_artist"

    def test_get(self):
        self.dynamo_db_sdk.get_item = MagicMock(return_value={})
        response = self.dynamo_db.get(self.key, self.value)
        self.assertDictEqual(response, {})

        self.dynamo_db_sdk.get_item = MagicMock(
            return_value=mock_dynamo_db.response
        )
        response = self.dynamo_db.get(self.key, self.value)
        self.assertDictEqual(response, mock_dynamo_db.response["Item"])

    def test_create(self):
        self.dynamo_db_sdk.put_item = MagicMock(return_value={})
        response = self.dynamo_db.create(
            key_name=self.key, key_value=self.value, songs=mock_dynamo_db.songs
        )

        self.dynamo_db_sdk.put_item.assert_called_with(
            Item={
                "artist_name": "some_artist",
                "transaction_id": response,
                "songs": mock_dynamo_db.songs,
            }
        )
