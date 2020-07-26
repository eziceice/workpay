import json
from service import UserService
from exception_handler import exception_handler_on_error


@exception_handler_on_error
def create_user(event, context):
    request_body = json.loads(event['body'])
    user_id = event['requestContext']['requestId']
    user_service = UserService()
    user_service.add_user(id=user_id, body=request_body)
    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': 'User has been created in the system'})
    }


def get_users(event, context):
    user_service = UserService()
    users = user_service.get_users()
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(users)
    }