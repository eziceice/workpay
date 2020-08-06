import functools
import json
import logging

from botocore.exceptions import ClientError

from exception import AssemblyPaymentError, ResourceNotFoundError


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
                'body': json.dumps({'message': str(err)})
            }
        except ResourceNotFoundError as err:
            logging.info(f'event = {event}')
            logging.exception(err)
            return {
                'statusCode': err.http_status,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': str(err)})
            }
        except ClientError as err:
            logging.info(f'event = {event}')
            logging.exception(err.response['Error']['Message'])
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': "Could not send SMS, please contact the system support"})
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
