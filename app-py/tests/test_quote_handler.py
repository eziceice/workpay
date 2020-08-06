from unittest import TestCase
from mock import patch

from quote_handler import create_quote, get_quote
from service import QuoteService
import pathlib
import json


class TestQuoteHandlerFunction(TestCase):
    @patch.object(QuoteService, 'add_quote')
    def test_create_quote_succeed(self, fake_add_quote):
        fake_add_quote.return_value = None
        with open(f'{pathlib.Path(__file__).parent}/resources/create_quote_input.json') as f:
            event = json.loads(f.read())
            response = create_quote(event=event, context='')

        self.assertEqual(response['statusCode'], 201)
        self.assertEqual(json.loads(response['body'])['quote_id'], '18d0de88-a44c-458a-bfb0-3c85aa3ab956')
        fake_add_quote.assert_called_with(quote_id='18d0de88-a44c-458a-bfb0-3c85aa3ab956',
                                          body={'number': '3', 'name': 'Test Quote', 'description': 'test description',
                                                'amount': '500', 'company_id': 'kk9982-a44c-458a-bfb0-3c85aa3ab956',
                                                'currency': 'AUD'})

    @patch.object(QuoteService, 'add_quote')
    def test_create_quote_failed(self, fake_add_quote):
        fake_add_quote.side_effect = Exception('Unknown Exception Occurred')
        with open(f'{pathlib.Path(__file__).parent}/resources/create_quote_input.json') as f:
            event = json.loads(f.read())
            response = create_quote(event=event, context='')

        self.assertEqual(response['statusCode'], 500)
        self.assertEqual(json.loads(response['body'])['message'], 'Unknown error occurred')
        fake_add_quote.assert_called_with(quote_id='18d0de88-a44c-458a-bfb0-3c85aa3ab956',
                                          body={'number': '3', 'name': 'Test Quote', 'description': 'test description',
                                                'amount': '500', 'company_id': 'kk9982-a44c-458a-bfb0-3c85aa3ab956',
                                                'currency': 'AUD'})

    @patch.object(QuoteService, 'get_quote')
    def test_get_quote_succeed(self, fake_get_quote):
        fake_get_quote.return_value = '1234567890'
        with open(f'{pathlib.Path(__file__).parent}/resources/get_quote_input.json') as f:
            event = json.loads(f.read())
            response = get_quote(event=event, context='')
            print(response)

        # self.assertEqual(response['statusCode'], 201)
        # self.assertEqual(json.loads(response['body'])['quote_id'], '18d0de88-a44c-458a-bfb0-3c85aa3ab956')
        # fake_add_quote.assert_called_with(quote_id='18d0de88-a44c-458a-bfb0-3c85aa3ab956',
        #                                   body={'number': '3', 'name': 'Test Quote', 'description': 'test description',
        #                                         'amount': '500', 'company_id': 'kk9982-a44c-458a-bfb0-3c85aa3ab956',
        #                                         'currency': 'AUD'})
