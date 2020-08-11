import json
from support.service import UserService
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


@exception_handler_on_error
def get_users(event, context):
    try:
        user_type = event['queryStringParameters'].get('type')
        user_email = event['queryStringParameters'].get('email')
    except AttributeError as e:
        user_type = None
        user_email = None
    user_service = UserService()
    if user_type is not None:
        response = user_service.get_users(query_name='type', query_value=user_type.upper())
    elif user_email is not None:
        response = user_service.get_users(query_name='email', query_value=user_email)
    else:
        response = user_service.get_users('', '', get_all=True)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }


@exception_handler_on_error
def update_user(event, context):
    user_id = event['pathParameters']['user_id']
    request_body = json.loads(event['body'])
    user_service = UserService()
    user_service.update_user(user_id=user_id, body=request_body)
    return {
        'statusCode': 204,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps('')
    }
