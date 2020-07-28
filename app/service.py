from db import DynamoDB
from typing import (
    Dict,
    Any,
    List
)
from utils import AppProperties
from requests.auth import HTTPBasicAuth
from exception_handler import (
    AssemblyPaymentError,
    ResourceNotFoundError
)
import requests
import json


class UserService:
    def __init__(self):
        properties = AppProperties()
        self.dynamodb = DynamoDB()
        self.payment_gw = AssemblyPaymentService(url=f'{properties.assembly_payment_url}/users')
        self.table_name = f'{properties.org}-{properties.env}-user-table'

    def add_user(self, user_id: str, body: Dict[str, Any]):
        db_user_item = self.build_db_user_item(user_id, body)
        gw_user_item = self.build_payment_gw_user_item(user_id, body)
        self.payment_gw.add_user(gw_user_item)
        self.dynamodb.add_item(table_name=self.table_name, item=db_user_item)

    @classmethod
    def build_db_user_item(cls, user_id, body):
        return {
            'id': user_id,
            'first_name': body['first_name'],
            'last_name': body['last_name'],
            'email': body['email'],
            'mobile': body['mobile'],
            'country': body['country'].upper(),
            'type': body['type'].upper()
        }

    @classmethod
    def build_payment_gw_user_item(cls, user_id, body):
        return {
            'id': user_id,
            'first_name': body['first_name'],
            'last_name': body['last_name'],
            'email': body['email'],
            'mobile': body['mobile'],
            'country': body['country'].upper(),
        }


class CompanyService:
    def __init__(self):
        properties = AppProperties()
        self.dynamodb = DynamoDB()
        self.payment_gw = AssemblyPaymentService(url=f'{properties.assembly_payment_url}/companies')
        self.table_name = f'{properties.org}-{properties.env}-company-table'

    def add_company(self, body: Dict[str, Any]):
        gw_company_item = self.build_payment_gw_company_item(body)
        company_id = self.payment_gw.add_company(gw_company_item)
        db_company_item = self.build_db_company_item(company_id, body)
        self.dynamodb.add_item(table_name=self.table_name, item=db_company_item)
        return company_id

    def get_companies(self) -> List[Dict[str, Any]]:
        return self.dynamodb.get_items(table_name=self.table_name)

    def get_company(self, company_id: str):
        result = self.dynamodb.get_item(table_name=self.table_name, item_id=company_id)
        if len(result) == 0:
            raise ResourceNotFoundError(f"Can not found company with given id - {company_id}", 404)
        return result

    @classmethod
    def build_db_company_item(cls, company_id, body):
        return {
            'id': company_id,
            'user_id': body['user_id'],
            'business_name': body['business_name'],
            'tax_number': body['tax_number'],
            'service': body['service'],
            'address_line1': body['address_line1'],
            'suburb': body['suburb'],
            'postcode': body['postcode'],
            'country': body['country'].upper()
        }

    @classmethod
    def build_payment_gw_company_item(cls, body):
        return {
            'user_id': body['user_id'],
            'name': body['business_name'],
            'legal_name': body['business_name'],
            'tax_number': body['tax_number'],
            'address_line1': body['address_line1'],
            'city': body['suburb'],
            'zip': body['postcode'],
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
            raise AssemblyPaymentError("Error in AssemblyPayment", response.status_code, response.content)

    def add_company(self, data):
        response = requests.post(self.url, data=json.dumps(data), headers=self.headers,
                                 auth=HTTPBasicAuth(self.username, self.api_key))
        # TODO: process exception if user creation failed
        if response.status_code == 201:
            company_id = json.loads(response.content)['companies']['id']
            return company_id
        else:
            raise AssemblyPaymentError("Error in AssemblyPayment", response.status_code, response.content)
