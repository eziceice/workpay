import json
from service import UserService
from exception_handler import exception_handler_on_error


@exception_handler_on_error
def create_user(event, context):
    request_body = json.loads(event['body'])
    user_id = event['requestContext']['requestId']
    user_details = build_user_details(user_id, request_body)
    user_service = UserService()
    user_service.add_user(user_detail=user_details)
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


def build_user_details(id, body):
    return {
        'id': {'S': id},
        'name': {'S': body['name']},
        'email': {'S': body['email']},
        'phone': {'S': body['phone']}
    }
