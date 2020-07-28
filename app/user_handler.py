import json
from service import UserService
from exception_handler import exception_handler_on_error


@exception_handler_on_error
def create_user(event, context):
    request_body = json.loads(event['body'])
    user_id = event['requestContext']['requestId']
    user_service = UserService()
    user_service.add_user(user_id=user_id, body=request_body)
    response = {'user_id': f'{user_id}'}
    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }