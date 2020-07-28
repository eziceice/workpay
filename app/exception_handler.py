import functools
import json
import logging


class AssemblyPaymentError(Exception):
    def __init__(self, message, http_status: int, content):
        super().__init__(message)
        self.http_status = http_status
        self.content = content
        self.message = message


class ResourceNotFoundError(Exception):
    def __init__(self, message, http_status: int):
        super().__init__(message)
        self.message = message
        self.http_status = http_status


def exception_handler_on_error(handler):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    @functools.wraps(handler)
    def wrapper(event, context):
        try:
            return handler(event, context)
        except KeyError:
            logging.info(f'event = {event}')
            logging.exception('KeyError occurred')
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'Some mandatory fields are missing!'})
            }
        except AssemblyPaymentError as error:
            logging.info(f'event = {event}')
            logging.exception(f'Received {error.http_status} from AssemblyPayment, content {error.content}')
            return {
                'statusCode': error.http_status,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'Something went wrong in the payment gateway'})
            }
        except ResourceNotFoundError as error:
            logging.info(f'event = {event}')
            logging.exception(error.message)
            return {
                'statusCode': error.http_status,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': f'{error.message}'})
            }
        except Exception:
            logging.info(f'event = {event}')
            logging.exception(f'Unknown Exception')
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'Unknown exception occurred'})
            }

    return wrapper
