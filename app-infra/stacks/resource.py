from enum import Enum


class LambdaFunction(Enum):
    CREATE_USER = 'create-user'
    CREATE_COMPANY = 'create-company'
    GET_COMPANY = 'get-company'
    GET_COMPANIES = 'get-companies'
