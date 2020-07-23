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

        self.rest_api = apigw.RestApi(self, id="API", rest_api_name=f"{props.owner}-{props.env}-api",
                                      endpoint_types=[apigw.EndpointType.REGIONAL], cloud_watch_role=True,
                                      deploy_options=apigw.StageOptions(logging_level=apigw.MethodLoggingLevel.INFO,
                                                                        metrics_enabled=True,
                                                                        tracing_enabled=True, stage_name=props.env))
        v1_resource = self.create_api_v1_resource()
        self.create_api_v1_user_resource(v1_resource, functions)

    def create_api_v1_resource(self):
        v1_resource = apigw.Resource(self, id="APIv1Resource", path_part="v1", parent=self.rest_api.root)
        return v1_resource

    def create_api_v1_user_resource(self, parent_resource, functions):
        user_resource = apigw.Resource(self, id="APIv1UserResource", path_part="users", parent=parent_resource)

        # Create User
        apigw.Method(self, id="CreateUserMethod", http_method="POST", resource=user_resource,
                     integration=apigw.LambdaIntegration(functions[LambdaFunction.CREATE_USER], proxy=True))
