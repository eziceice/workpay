from unittest import TestCase
from mock import patch, Mock

from exception_handler import AssemblyPaymentError
from service import CompanyService
from company_handler import create_company, get_company
import pathlib
import json


class TestUserHandlerFunction(TestCase):

    @patch.object(CompanyService, 'add_company')
    def test_create_company_succeed(self, fake_add_company):
        fake_add_company.return_value = '1234567890'
        with open(f'{pathlib.Path(__file__).parent}/resources/create_company_input.json') as f:
            event = json.loads(f.read())
            response = create_company(event=event, context='')
            print(response)

        self.assertEqual(response['statusCode'], 201)
        self.assertEqual(json.loads(response['body'])['company_id'], '1234567890')
        fake_add_company.assert_called_with(
            body={'user_id': '18d0de88-a44c-458a-bfb0-3c85aa3ab956', 'business_name': 'ABC Company',
                  'tax_number': '12345', 'address_line1': '100 Collins Street', 'country': 'AUS', 'suburb': 'Docklands',
                  'postcode': '3008'})

    @patch.object(CompanyService, 'add_company')
    def test_create_company_failed(self, fake_add_company):
        fake_add_company.side_effect = AssemblyPaymentError(Mock("Error"), '401', 'Bad credentials')
        with open(f'{pathlib.Path(__file__).parent}/resources/create_company_input.json') as f:
            event = json.loads(f.read())
            response = create_company(event=event, context='')

        self.assertEqual(response['statusCode'], '401')
        self.assertEqual(json.loads(response['body'])['message'], 'Something went wrong in the payment gateway')
        fake_add_company.assert_called_with(
            body={'user_id': '18d0de88-a44c-458a-bfb0-3c85aa3ab956', 'business_name': 'ABC Company',
                  'tax_number': '12345', 'address_line1': '100 Collins Street', 'country': 'AUS', 'suburb': 'Docklands',
                  'postcode': '3008'})

    @patch.object(CompanyService, 'get_company')
    def test_create_company_succeed(self, fake_get_company):
        fake_get_company.return_value = '1234567890'
        with open(f'{pathlib.Path(__file__).parent}/resources/get_company_input.json') as f:
            event = json.loads(f.read())
            response = get_company(event=event, context='')

