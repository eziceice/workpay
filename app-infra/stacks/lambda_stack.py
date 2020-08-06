from typing import Dict

from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3
)
from stacks.resource import LambdaFunction

import stacks.properties as props


class LambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_full_access_role = iam.Role(self, id='LambdaFullAccessRole',
                                           role_name=f'{props.org}-{props.env}-lambda-full-access-role',
                                           assumed_by=iam.ServicePrincipal(
                                               'lambda.amazonaws.com', region=props.aws_region),
                                           managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                                               'AWSLambdaFullAccess')])
        iam.Policy(self, id='SendSMSPolicy', policy_name='LambdaSendSMSPolicy', roles=[lambda_full_access_role],
                   statements=[iam.PolicyStatement(actions=['mobiletargeting:SendMessages'], resources=['*'])])

        lambda_python_bucket = s3.Bucket.from_bucket_name(self, id='LambdaPythonResourcesBucket',
                                                          bucket_name=f'{props.org}-python-lambda-resources')

        self.create_user_function = _lambda.Function(
            self, id='CreateUserFunction',
            function_name=f'{props.org}-{props.env}-create-user-function',
            runtime=_lambda.Runtime.PYTHON_3_8,
            timeout=core.Duration.seconds(10),
            code=_lambda.Code.from_bucket(bucket=lambda_python_bucket,
                                          key=props.lambda_python_version),
            handler='user_handler.create_user',
            role=lambda_full_access_role
        )

        self.get_users_function = _lambda.Function(
            self, id='GetUsersFunction',
            function_name=f'{props.org}-{props.env}-get-users-function',
            runtime=_lambda.Runtime.PYTHON_3_8,
            timeout=core.Duration.seconds(10),
            code=_lambda.Code.from_bucket(bucket=lambda_python_bucket,
                                          key=props.lambda_python_version),
            handler='user_handler.get_users',
            role=lambda_full_access_role
        )

        self.create_company_function = _lambda.Function(
            self, id='CreateCompanyFunction',
            function_name=f'{props.org}-{props.env}-create-company-function',
            runtime=_lambda.Runtime.PYTHON_3_8,
            timeout=core.Duration.seconds(10),
            code=_lambda.Code.from_bucket(bucket=lambda_python_bucket,
                                          key=props.lambda_python_version),
            handler='company_handler.send_sms',
            role=lambda_full_access_role
        )

        self.get_companies_function = _lambda.Function(
            self, id='GetCompaniesFunction',
            function_name=f'{props.org}-{props.env}-get-companies-function',
            runtime=_lambda.Runtime.PYTHON_3_8,
            timeout=core.Duration.seconds(10),
            code=_lambda.Code.from_bucket(bucket=lambda_python_bucket,
                                          key=props.lambda_python_version),
            handler='company_handler.get_companies',
            role=lambda_full_access_role
        )

        self.get_company_function = _lambda.Function(
            self, id='GetCompanyFunction',
            function_name=f'{props.org}-{props.env}-get-company-function',
            runtime=_lambda.Runtime.PYTHON_3_8,
            timeout=core.Duration.seconds(10),
            code=_lambda.Code.from_bucket(bucket=lambda_python_bucket,
                                          key=props.lambda_python_version),
            handler='company_handler.get_company',
            role=lambda_full_access_role
        )

        self.create_quote_function = _lambda.Function(
            self, id='CreateQuoteFunction',
            function_name=f'{props.org}-{props.env}-create-quote-function',
            runtime=_lambda.Runtime.PYTHON_3_8,
            timeout=core.Duration.seconds(10),
            code=_lambda.Code.from_bucket(bucket=lambda_python_bucket,
                                          key=props.lambda_python_version),
            handler='quote_handler.create_quote',
            role=lambda_full_access_role
        )

        self.send_sms_function = _lambda.Function(
            self, id='SendSMSFunction',
            function_name=f'{props.org}-{props.env}-send-sms-function',
            runtime=_lambda.Runtime.PYTHON_3_8,
            timeout=core.Duration.seconds(10),
            code=_lambda.Code.from_bucket(bucket=lambda_python_bucket,
                                          key=props.lambda_python_version),
            handler='sms_handler.send_sms',
            role=lambda_full_access_role
        )

    @property
    def functions(self) -> Dict[LambdaFunction, _lambda.Function]:
        return {
            LambdaFunction.CREATE_USER: self.create_user_function,
            LambdaFunction.CREATE_COMPANY: self.create_company_function,
            LambdaFunction.GET_COMPANIES: self.get_companies_function,
            LambdaFunction.GET_COMPANY: self.get_company_function,
            LambdaFunction.CREATE_QUOTE: self.create_quote_function,
            LambdaFunction.GET_USERS: self.get_users_function,
            LambdaFunction.SEND_SMS: self.send_sms_function
        }
