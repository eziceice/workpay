import json
import pathlib
import unittest
import uuid

import boto3
import utils
from unittest import TestCase
from moto import mock_dynamodb2
from user_handler import (
    create_user,
    get_users
)


def mock_dynamodb_client(table_name, key):
    client = boto3.client('dynamodb')
    client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': key,
                'AttributeType': 'S'
            },
        ],
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': key,
                'KeyType': 'HASH'
            },
        ])
    return client


def mock_users_data(client, table_name):
    for x in range(5):
        client.put_item(TableName=table_name, Item={
            'id': {'S': str(uuid.uuid4())},
            'name': {'S': 'MJ'},
            'email': {'S': 'MJ@125.com'},
            'phone': {'S': f'0444004{x}'}
        })


class TestUserHandlerFunction(TestCase):

    def setUp(self) -> None:
        properties = utils.get_properties()
        org = properties['org']
        env = properties['env']
        self.table_name = f'{org}-{env}-user-table'

    @mock_dynamodb2
    def test_create_user_succeed(self):
        mock_client = mock_dynamodb_client(
            table_name=self.table_name, key='id')
        with open(f'{pathlib.Path(__file__).parent}/resources/create_user_input.json') as f:
            data = json.loads(f.read())
            create_user(data, '')
        assert len(mock_client.scan(TableName=self.table_name)['Items']) == 1

    @mock_dynamodb2
    def test_get_user_succeed(self):
        mock_client = mock_dynamodb_client(
            table_name=self.table_name, key='id')
        mock_users_data(mock_client, table_name=self.table_name)
        print(get_users('', ''))


if __name__ == '__main__':
    unittest.main()
