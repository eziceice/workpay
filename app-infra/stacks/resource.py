from enum import Enum


class LambdaFunction(Enum):
    CREATE_USER = 'create-user'
    CREATE_COMPANY = 'create-company'
    GET_COMPANY = 'get-company'
    GET_COMPANIES = 'get-companies'
    CREATE_QUOTE = 'create-quote'
    GET_USERS = 'get-users'
    SEND_SMS = 'send-sms'
    CREATE_SUBBY = 'create-subby'
    UPDATE_USER = 'update-user'
