import os
from uuid import uuid4

import boto3

AWS_ACCESS_KEY_ID = os.environ.get("aws_access_key_id")
AWS_SECRET_ACCESS_KEY = os.environ.get("aws_secret_access_key")
REGION_NAME = os.environ.get("region_name", "us-east-2")


class DynamoDb:
    def __init__(self, table_name):
        self.table_name = table_name
        self.client = boto3.resource(
            "dynamodb",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION_NAME,
        )
        self.dynamo_db = self.client.Table(table_name)

    def get(self, key_name, key_value):
        response = self.dynamo_db.get_item(Key={key_name: key_value})
        return response["item"]

    def create(self, key_name, key_value, **kwargs):
        transaction_id = uuid4()
        return self.dynamo_db.put_item(
            Item={
                key_name: key_value,
                "transaction_id": transaction_id.hex,
                **kwargs,
            }
        )

    def update(self, key_name, key_value, songs):
        return self.dynamo_db.put_item(
            Item={key_name: key_value},
            UpdateExpression="SET songs=:val1",
            ExpressionAttributeValues={":val1": songs},
        )
