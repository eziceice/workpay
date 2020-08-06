import json
from exception_handler import exception_handler_on_error
from service import SMSService


@exception_handler_on_error
def send_sms(event, context):
    request_body = json.loads(event['body'])
    sms_service = SMSService()
    response = sms_service.send_message(request_body)
    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }
