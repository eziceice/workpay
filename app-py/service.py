import logging
from datetime import date

import boto3
from boto3.dynamodb.conditions import Attr

from db import DynamoDB
from typing import (
    Dict,
    Any,
    List
)
from utils import AppProperties
from requests.auth import HTTPBasicAuth
from exception import (
    AssemblyPaymentError,
    ResourceNotFoundError,
    AssemblyPaymentAuthError)
import requests
import json


class UserService:
    def __init__(self):
        properties = AppProperties()
        self.dynamodb = DynamoDB()
        self.payment_gw = AssemblyPaymentService()
        self.table_name = f'{properties.org}-{properties.env}-user-table'

    def add_user(self, user_id: str, body: Dict[str, Any]):
        db_user_item = self.build_db_item(user_id, body)
        gw_user_item = self.build_payment_gw_item(user_id, body)
        self.payment_gw.add_user(gw_user_item, endpoint='users')
        self.dynamodb.add_item(table_name=self.table_name, item=db_user_item)

    def get_users(self, user_type):
        user_filter = Attr('type').eq(user_type)
        result = self.dynamodb.get_items(self.table_name, item_filter=user_filter)
        if len(result) == 0:
            raise ResourceNotFoundError(f'Can not found any {user_type} in the system', 404)
        return result

    @classmethod
    def build_db_item(cls, user_id, body):
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
    def build_payment_gw_item(cls, user_id, body):
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
        self.payment_gw = AssemblyPaymentService()
        self.table_name = f'{properties.org}-{properties.env}-company-table'
        self.user_table_name = f'{properties.org}-{properties.env}-user-table'

    def add_company(self, body: Dict[str, Any]):
        company_id = ''
        gw_company_item = self.build_payment_gw_item(body)
        db_company_item = self.build_db_item(company_id, body)
        company_id = self.payment_gw.add_company(gw_company_item, endpoint='companies')
        db_company_item['id'] = company_id
        self.dynamodb.add_item(table_name=self.table_name, item=db_company_item)
        self.dynamodb.update_item(table_name=self.user_table_name, key=body['user_id'], attribute_value=company_id,
                                  attribute_name='company_id')
        return company_id

    def get_companies(self) -> List[Dict[str, Any]]:
        result = self.dynamodb.get_items(table_name=self.table_name)
        if len(result) == 0:
            raise ResourceNotFoundError(f'Can not found any companies in the system', 404)
        return result

    def get_company(self, company_id: str):
        result = self.dynamodb.get_item(table_name=self.table_name, key='id', item_id=company_id)
        if len(result) == 0:
            raise ResourceNotFoundError(f'Can not found company with given id - {company_id} in the system', 404)
        return result

    @classmethod
    def build_db_item(cls, company_id, body):
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
    def build_payment_gw_item(cls, body):
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


class QuoteService:
    def __init__(self):
        properties = AppProperties()
        self.dynamodb = DynamoDB()
        self.payment_gw = AssemblyPaymentService()
        self.table_name = f'{properties.org}-{properties.env}-quote-table'

    def add_quote(self, quote_id: str, body: Dict[str, Any]):
        db_quote_item = self.build_db_item(quote_id, body)
        self.dynamodb.add_item(table_name=self.table_name, item=db_quote_item)

    def get_quote(self, quote_id: str):
        result = self.dynamodb.get_item(table_name=self.table_name, key='id', item_id=quote_id)
        if len(result) == 0:
            raise ResourceNotFoundError(f'Can not found quote with given id - {quote_id} in the system', 404)
        return result

    @classmethod
    def build_db_item(cls, quote_id, body):
        return {
            'id': quote_id,
            'number': body['number'],
            'name': body['name'],
            'description': body['description'],
            'amount': body['amount'],
            'company_id': body['company_id'],
            'currency': body['currency'].upper(),
            'timestamp': date.today().strftime("%d/%m/%Y")
        }


class AssemblyPaymentService:
    def __init__(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        properties = AppProperties()
        self.url = properties.assembly_payment_url
        # TODO: user environment variable
        self.username = "zailconsulting@gmail.com"
        self.api_key = "ZWRhNTA3YWY0YTJhZDdlNGU1ZWQzNGYzYTRmZjY4MzI="
        self.headers = {'accept': 'application/json',
                        'content-type': 'application/json'}

    def add_user(self, data, endpoint):
        # TODO: create a wrapper for handle request and response to assembly payment
        try:
            response = requests.post(f'{self.url}/{endpoint}', data=json.dumps(data), headers=self.headers,
                                     auth=HTTPBasicAuth(self.username, self.api_key))
        except requests.exceptions.RequestException:
            logging.exception(f'Failed to connect Assembly Payment')
            raise AssemblyPaymentError(AssemblyPaymentError.CONNECTION_ERROR, 504)

        if response.status_code == 201:
            logging.info(f'Receiving successful response from Assembly Payment: {response.content}')
        else:
            self.handle_response_error(response.status_code, response.content)

    def add_company(self, data, endpoint):
        try:
            response = requests.post(f'{self.url}/{endpoint}', data=json.dumps(data), headers=self.headers,
                                     auth=HTTPBasicAuth(self.username, self.api_key))
        except requests.exceptions.RequestException:
            logging.exception(f'Failed to connect Assembly Payment')
            raise AssemblyPaymentError(AssemblyPaymentError.CONNECTION_ERROR, 504)

        if response.status_code == 201:
            logging.info(f'Receiving successful response from Assembly Payment: {response.content}')
            company_id = json.loads(response.content)['companies']['id']
            return company_id
        else:
            self.handle_response_error(response.status_code, response.content)

    def add_quote(self, data, endpoint):
        try:
            response = requests.post(f'{self.url}/{endpoint}', data=json.dumps(data), headers=self.headers,
                                     auth=HTTPBasicAuth(self.username, self.api_key))
        except requests.exceptions.RequestException:
            logging.exception(f'Failed to connect Assembly Payment')
            raise AssemblyPaymentError(AssemblyPaymentError.CONNECTION_ERROR, 504)
        # TODO: process exception if user creation failed
        if response.status_code == 201:
            quote_id = json.loads(response.content)['items']['id']
            return quote_id
        else:
            self.handle_response_error(response.status_code, response.content)

    def handle_response_error(self, status_code: int, content):
        if status_code in (401, 403):
            logging.error(
                f'Assembly Payment authentication error, response code: {status_code}, response content: {content}')
            raise AssemblyPaymentAuthError(AssemblyPaymentError.SYSTEM_ERROR, 500, content)

        if status_code == 500:
            logging.error(
                f'Assembly Payment internal server error, response code: {status_code}, response content: {content}')
            raise AssemblyPaymentError(AssemblyPaymentError.SYSTEM_ERROR, 500, content)


class SMSService:
    def __init__(self):
        self.client = boto3.client('pinpoint')
        self.application_id = 'dc0bd061a34a427c961760a3db8eee32'  # TODO: use env var

    def send_message(self, request_body):
        destination_number = request_body['destination_number']
        message_type = 'TRANSACTIONAL'
        sender_id = 'WorkPay'
        raw_response = self.client.send_messages(
            ApplicationId=self.application_id,
            MessageRequest={
                'Addresses': {
                    destination_number: {
                        'ChannelType': 'SMS'
                    }
                },
                'MessageConfiguration': {
                    'SMSMessage': {
                        'Body': request_body['message'],
                        'MessageType': message_type,
                        'SenderId': sender_id
                    }
                }
            }
        )
        return {'message-id': raw_response['MessageResponse']['Result'][destination_number]['MessageId']}
