import json
from service import QuoteService
from exception_handler import exception_handler_on_error


@exception_handler_on_error
def create_quote(event, context):
    quote_id = event['requestContext']['requestId']
    request_body = json.loads(event['body'])
    quote_service = QuoteService()
    quote_service.add_quote(quote_id=quote_id, body=request_body)
    response = {'quote_id': quote_id}
    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }
