import unittest
from unittest import TestCase
from mock import patch

from exception_handler import AssemblyPaymentError
from support.service import CompanyService
from company_handler import create_company, get_company, get_companies
from exception_handler import ResourceNotFoundError
import pathlib
import json


class TestCompanyHandlerFunction(TestCase):

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
        fake_add_company.side_effect = AssemblyPaymentError(AssemblyPaymentError.SYSTEM_ERROR, 500, 'Bad credentials')
        with open(f'{pathlib.Path(__file__).parent}/resources/create_company_input.json') as f:
            event = json.loads(f.read())
            response = create_company(event=event, context='')

        self.assertEqual(response['statusCode'], 500)
        self.assertEqual(json.loads(response['body'])['message'], AssemblyPaymentError.SYSTEM_ERROR)
        fake_add_company.assert_called_with(
            body={'user_id': '18d0de88-a44c-458a-bfb0-3c85aa3ab956', 'business_name': 'ABC Company',
                  'tax_number': '12345', 'address_line1': '100 Collins Street', 'country': 'AUS', 'suburb': 'Docklands',
                  'postcode': '3008'})

    @patch.object(CompanyService, 'get_company')
    def test_get_company_succeed(self, fake_get_company):
        mock_response_body = {
            "business_name": "Y Business 1",
            "service": "test-service",
            "tax_number": "123456789",
            "user_id": "1b62e34a-bc7a-4093-876f-004d5dfc011f",
            "address_line1": "test address 1",
            "postcode": "3008",
            "suburb": "docklands",
            "id": "d34a6800-b23a-0138-7995-0a58a9feac03",
            "country": "AUS"
        }
        fake_get_company.return_value = [mock_response_body]
        with open(f'{pathlib.Path(__file__).parent}/resources/get_company_input.json') as f:
            event = json.loads(f.read())
            response = get_company(event=event, context='')
            print(response)

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body'])['business_name'], mock_response_body['business_name'])
        self.assertEqual(json.loads(response['body'])['service'], mock_response_body['service'])
        self.assertEqual(json.loads(response['body'])['tax_number'], mock_response_body['tax_number'])
        self.assertEqual(json.loads(response['body'])['user_id'], mock_response_body['user_id'])
        fake_get_company.assert_called_with(company_id='6521ff6f-b441-4ef9-97e9-c54c077836ea')

    @patch.object(CompanyService, 'get_company')
    def test_get_company_failed_with_resource_not_found_error(self, fake_get_company):
        fake_get_company.side_effect = ResourceNotFoundError('Can not find company id xyz', 404)
        with open(f'{pathlib.Path(__file__).parent}/resources/get_company_input.json') as f:
            event = json.loads(f.read())
            response = get_company(event=event, context='')

        self.assertEqual(json.loads(response['body'])['message'], 'Can not find company id xyz')
        self.assertEqual(response['statusCode'], 404)
        fake_get_company.assert_called_with(company_id='6521ff6f-b441-4ef9-97e9-c54c077836ea')

    @patch.object(CompanyService, 'get_companies')
    def test_get_companies_succeed(self, fake_get_companies):
        mock_response_body1 = {
            "business_name": "Y Business 1",
            "service": "test-service",
            "tax_number": "123456789",
            "user_id": "1b62e34a-bc7a-4093-876f-004d5dfc011f",
            "address_line1": "test address 1",
            "postcode": "3008",
            "suburb": "docklands",
            "id": "d34a6800-b23a-0138-7995-0a58a9feac03",
            "country": "AUS"
        }
        mock_response_body2 = {
            "business_name": "Y Business 1",
            "service": "test-service",
            "tax_number": "123456789",
            "user_id": "1b62e34a-bc7a-4093-876f-004d5dfc011f",
            "address_line1": "test address 1",
            "postcode": "3008",
            "suburb": "docklands",
            "id": "d34a6800-b23a-0138-7995-0a58a9feac03",
            "country": "AUS"
        }
        fake_get_companies.return_value = [mock_response_body1, mock_response_body2]
        response = get_companies(event='', context='')

        self.assertEqual(len(json.loads(response['body'])), 2)
        self.assertEqual(response['statusCode'], 200)
        fake_get_companies.assert_called_with()

    @patch.object(CompanyService, 'get_companies')
    def test_get_companies_failed_with_resource_not_found_error(self, fake_get_companies):
        fake_get_companies.side_effect = ResourceNotFoundError('Can not found any companies in the system', 404)
        response = get_companies('', '')

        self.assertEqual(json.loads(response['body'])['message'], 'Can not found any companies in the system')
        self.assertEqual(response['statusCode'], 404)
        fake_get_companies.assert_called_with()


if __name__ == '__main__':
    unittest.main()