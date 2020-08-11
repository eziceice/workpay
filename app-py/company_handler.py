import json
from support.service import CompanyService
from exception_handler import exception_handler_on_error


@exception_handler_on_error
def create_company(event, context):
    request_body = json.loads(event['body'])
    company_service = CompanyService()
    company_id = company_service.add_company(body=request_body)
    response = {'company_id': company_id}
    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }


@exception_handler_on_error
def get_companies(event, context):
    company_service = CompanyService()
    response = company_service.get_companies()
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }


@exception_handler_on_error
def get_company(event, context):
    company_id = event['pathParameters']['company_id']
    company_service = CompanyService()
    response = company_service.get_company(company_id=company_id)[0]
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }
