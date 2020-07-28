import boto3
from typing import (
    Dict,
    Any
)

from boto3.dynamodb.conditions import Key


class DynamoDB:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def add_item(self, table_name: str, item: Dict[str, Any]):
        table = self.dynamodb.Table(table_name)
        table.put_item(Item=item)

    def get_items(self, table_name: str, item_filter=None):
        table = self.dynamodb.Table(table_name)
        if item_filter is None:
            return table.scan()['Items']
        return table.scan(FilterExpression=item_filter)['Items']

    def get_item(self, table_name: str, item_id: str):
        table = self.dynamodb.Table(table_name)
        return table.query(KeyConditionExpression=Key('id').eq(item_id))['Items']