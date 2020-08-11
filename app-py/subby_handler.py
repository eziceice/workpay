import json

from exception_handler import exception_handler_on_error
from support.resource import UserType
from support.service import UserService, CompanyService


@exception_handler_on_error
def create_subby(event, context):
    request_body = json.loads(event['body'])
    request_body['type'] = UserType.SELLER.name
    user_id = event['requestContext']['requestId']
    request_body['user_id'] = user_id
    user_service = UserService()
    company_service = CompanyService()
    user_service.add_user(user_id=user_id, body=request_body)
    company_service.add_company(body=request_body)
    response = {'user_id': user_id}
    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }
