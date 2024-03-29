from typing import Dict

from aws_cdk import (
    core,
    aws_apigateway as apigw,
    aws_lambda as _lambda
)

import stacks.properties as props
from stacks.resource import LambdaFunction


class APIGatewayStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, functions: Dict[LambdaFunction, _lambda.Function] = None,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.rest_api = apigw.RestApi(self, id='API', rest_api_name=f'{props.org}-{props.env}-api',
                                      endpoint_types=[apigw.EndpointType.REGIONAL], cloud_watch_role=True,
                                      deploy_options=apigw.StageOptions(logging_level=apigw.MethodLoggingLevel.INFO,
                                                                        metrics_enabled=True,
                                                                        tracing_enabled=True, stage_name=props.env))
        v1_resource = self.create_api_v1_resource()
        self.params_validator = apigw.RequestValidator(self, id='APIParamsValidator',
                                                       request_validator_name='ParamsValidator',
                                                       rest_api=self.rest_api, validate_request_parameters=True)
        self.create_api_v1_user_resource(v1_resource, functions)
        self.create_api_v1_company_resource(v1_resource, functions)
        self.create_api_v1_quote_resource(v1_resource, functions)
        self.create_api_v1_sms_resource(v1_resource, functions)
        self.create_api_v1_subby_resource(v1_resource, functions)

    def create_api_v1_resource(self):
        v1_resource = apigw.Resource(self, id='APIv1Resource', path_part='v1', parent=self.rest_api.root)
        return v1_resource

    def create_api_v1_user_resource(self, parent_resource, functions):
        user_resource = apigw.Resource(self, id='APIv1UserResource', path_part='users', parent=parent_resource)

        # Create User
        apigw.Method(self, id='CreateUserMethod', http_method='POST', resource=user_resource,
                     integration=apigw.LambdaIntegration(functions[LambdaFunction.CREATE_USER], proxy=True))

        # Get Users
        apigw.Method(self, id='GetUsersMethod', http_method='GET', resource=user_resource,
                     integration=apigw.LambdaIntegration(functions[LambdaFunction.GET_USERS], proxy=True),
                     options=apigw.MethodOptions(request_parameters={'method.request.querystring.type': False,
                                                                     'method.request.querystring.email': False},
                                                 request_validator=self.params_validator))

        # Update User from company_id
        user_id_resource = user_resource.add_resource(path_part="{user_id}")
        user_id_resource.add_method(http_method="PUT",
                                    integration=apigw.LambdaIntegration(functions[LambdaFunction.UPDATE_USER],
                                                                        proxy=True))

    def create_api_v1_company_resource(self, parent_resource, functions):
        company_resource = apigw.Resource(self, id='APIv1CompanyResource', path_part='companies',
                                          parent=parent_resource)

        # Create Company
        apigw.Method(self, id='CreateCompanyMethod', http_method='POST', resource=company_resource,
                     integration=apigw.LambdaIntegration(functions[LambdaFunction.CREATE_COMPANY], proxy=True))

        # Get Companies
        apigw.Method(self, id='GETCompaniesMethod', http_method='GET', resource=company_resource,
                     integration=apigw.LambdaIntegration(functions[LambdaFunction.GET_COMPANIES], proxy=True))

        # Get Company from company_id
        company_id_resource = company_resource.add_resource(path_part="{company_id}")
        company_id_resource.add_method(http_method="GET",
                                       integration=apigw.LambdaIntegration(functions[LambdaFunction.GET_COMPANY],
                                                                           proxy=True))

    def create_api_v1_quote_resource(self, parent_resource, functions):
        quote_resource = apigw.Resource(self, id='APIv1QuoteResource', path_part='quotes', parent=parent_resource)

        # Create Quote
        apigw.Method(self, id='CreateQuoteMethod', http_method='POST', resource=quote_resource,
                     integration=apigw.LambdaIntegration(functions[LambdaFunction.CREATE_QUOTE], proxy=True))

    def create_api_v1_sms_resource(self, parent_resource, functions):
        sms_resource = apigw.Resource(self, id='APIv1SMSeResource', path_part='sms', parent=parent_resource)

        # Send SMS
        apigw.Method(self, id='SendSMSMethod', http_method='POST', resource=sms_resource,
                     integration=apigw.LambdaIntegration(functions[LambdaFunction.SEND_SMS], proxy=True))

    def create_api_v1_subby_resource(self, parent_resource, functions):
        subby_resource = apigw.Resource(self, id='APIv1SubbyResource', path_part='subby', parent=parent_resource)

        # Create Subby
        apigw.Method(self, id='CreateSubbyMethod', http_method='POST', resource=subby_resource,
                     integration=apigw.LambdaIntegration(functions[LambdaFunction.CREATE_SUBBY], proxy=True))
