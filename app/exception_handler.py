import functools
import json


def exception_handler_on_error(handler):
    @functools.wraps(handler)
    def wrapper(event, context):
        try:
            return handler(event, context)
        except Exception as ex:
            print('event = %r' % event)
            print(ex)
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'Errors!'})
            }

    return wrapper
