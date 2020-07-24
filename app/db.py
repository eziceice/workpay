import boto3
from typing import (
    Dict,
    Any
)


class DynamoDB:
    def __init__(self):
        self.client = boto3.client('dynamodb')

    def add_item(self, table_name: str, item: Dict[str, Dict[str, Any]]):
        self.client.put_item(TableName=table_name, Item=item)

    def get_items(self, table_name: str):
        return self.client.scan(TableName=table_name)['Items']

