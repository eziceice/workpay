import json
import pathlib
import unittest
import uuid
from mock import patch, Mock
import boto3
import utils
from unittest import TestCase
from service import UserService
from moto import mock_dynamodb2
from user_handler import (
    create_user
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
            'first_name': {'S': 'Michael'},
            'last_name': {'S': 'Jordan'},
            'email': {'S': 'MJ@125.com'},
            'mobile': {'S': f'0444004{x}'},
            'country': {'S': 'AUS'},
            'type': {'S': 'Seller'}
        })


class TestUserHandlerFunction(TestCase):

    def setUp(self) -> None:
        properties = utils.AppProperties()
        self.table_name = f'{properties.org}-{properties.env}-user-table'

    @patch.object(UserService, 'add_user')
    def test_create_user_succeed(self, fake_add_user):
        # with patch.object(UserService, 'add_user') as mock_method:
        #     mock_method.return_value = None
        fake_add_user.return_value = None
        with open(f'{pathlib.Path(__file__).parent}/resources/create_user_input.json') as f:
            event = json.loads(f.read())
            response = create_user(event, '')

        self.assertEqual(response['statusCode'], 201)
        self.assertEqual(json.loads(response['body'])['user_id'], '18d0de88-a44c-458a-bfb0-3c85aa3ab956')
        fake_add_user.assert_called_with(user_id='18d0de88-a44c-458a-bfb0-3c85aa3ab956',
                                         body={'first_name': 'Yutian', 'last_name': 'Li8',
                                               'email': 'liyutian8@gmail.com', 'mobile': '0451777888', 'country': 'AUS',
                                               'type': 'seller'})

    @patch.object(UserService, 'add_user')
    def test_create_user_failed(self, fake_add_user):
        fake_add_user.side_effect = KeyError(Mock(status=400), 'user_id is missing!')
        with open(f'{pathlib.Path(__file__).parent}/resources/create_user_input.json') as f:
            data = json.loads(f.read())
            response = create_user(data, '')
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(json.loads(response['body'])['message'], 'Some mandatory fields are missing!')
        fake_add_user.assert_called_with(user_id='18d0de88-a44c-458a-bfb0-3c85aa3ab956',
                                         body={'first_name': 'Yutian', 'last_name': 'Li8',
                                               'email': 'liyutian8@gmail.com', 'mobile': '0451777888', 'country': 'AUS',
                                               'type': 'seller'})

    # For integration test
    # @mock_dynamodb2
    # def test_create_user_succeed(self):
    #     mock_client = mock_dynamodb_client(
    #         table_name=self.table_name, key='id')
    #     with open(f'{pathlib.Path(__file__).parent}/resources/create_user_input.json') as f:
    #         data = json.loads(f.read())
    #         create_user(data, '')
    #     assert len(mock_client.scan(TableName=self.table_name)['Items']) == 1
    #
    # @mock_dynamodb2
    # def test_get_user_succeed(self):
    #     mock_client = mock_dynamodb_client(
    #         table_name=self.table_name, key='id')
    #     mock_users_data(mock_client, table_name=self.table_name)
    #     print(get_users('', ''))


if __name__ == '__main__':
    unittest.main()
