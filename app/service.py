from db import DynamoDB
from typing import (
    Dict,
    Any,
    List
)
from utils import AppProperties
import requests
from requests.auth import HTTPBasicAuth
import json


class UserService:
    def __init__(self):
        properties = AppProperties()
        self.dynamodb = DynamoDB()
        self.payment_gw = AssemblyPaymentService(url=f'{properties.assembly_payment_url}/users')
        self.table_name = f'{properties.org}-{properties.env}-user-table'

    def add_user(self, id: str, body: Dict[str, Any]):
        db_user_item = self.build_db_user_item(id, body)
        gw_user_item = self.build_payment_gw_user_item(id, body)
        self.payment_gw.add_user(gw_user_item)
        self.dynamodb.add_item(table_name=self.table_name, item=db_user_item)

    def get_users(self) -> List[Dict[str, Any]]:
        return self.dynamodb.get_items(table_name=self.table_name)

    @classmethod
    def build_db_user_item(cls, id, body):
        return {
            'id': {'S': id},
            'first_name': {'S': body['first_name']},
            'last_name': {'S': body['last_name']},
            'email': {'S': body['email']},
            'mobile': {'S': body['mobile']},
            'country': {'S': body['country'].upper()},
            'type': {'S': body['type'].upper()}
        }

    @classmethod
    def build_payment_gw_user_item(cls, id, body):
        return {
            'id': id,
            'first_name': body['first_name'],
            'last_name': body['last_name'],
            'email': body['email'],
            'mobile': body['mobile'],
            'country': body['country'].upper(),
        }


class AssemblyPaymentService:
    def __init__(self, url):
        self.url = url
        # TODO: user environment variable
        self.username = "zailconsulting@gmail.com"
        self.api_key = "ZWRhNTA3YWY0YTJhZDdlNGU1ZWQzNGYzYTRmZjY4MzI="
        self.headers = {'accept': 'application/json',
                        'content-type': 'application/json'}

    def add_user(self, data):
        response = requests.post(self.url, data=json.dumps(data), headers=self.headers,
                                 auth=HTTPBasicAuth(self.username, self.api_key))
        # TODO: process exception if user creation failed
        if response.status_code == 201:
            print(response.content)
        else:
            raise ConnectionError(response.content)
