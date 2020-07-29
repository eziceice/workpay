import functools
import json
import logging


class AssemblyPaymentError(Exception):
    def __init__(self, message, http_status: int, content=None):
        super().__init__(message)
        self.http_status = http_status
        self.content = content


class AssemblyPaymentAuthError(AssemblyPaymentError):
    def __init__(self, message, http_status: int, content):
        super().__init__(message, http_status, content)


class ResourceNotFoundError(Exception):
    def __init__(self, message, http_status: int):
        super().__init__(message)
        self.http_status = http_status


def exception_handler_on_error(handler):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    @functools.wraps(handler)
    def wrapper(event, context):
        try:
            return handler(event, context)
        except KeyError as err:
            logging.info(f'event = {event}')
            logging.exception(err)
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'Some mandatory fields are missing!'})
            }
        except AssemblyPaymentError as err:
            logging.info(f'event = {event}')
            return {
                'statusCode': err.http_status,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': err})
            }
        except ResourceNotFoundError as err:
            logging.info(f'event = {event}')
            logging.exception(err)
            return {
                'statusCode': err.http_status,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': err})
            }
        except Exception as e:
            logging.info(f'event = {event}')
            logging.exception(e)
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'Unknown error occurred'})
            }

    return wrapper
