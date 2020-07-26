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

        self.create_user_function = _lambda.Function(
            self, id='CreateUserFunction',
            function_name=f'{props.org}-{props.env}-create-user-function',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_bucket(bucket=s3.Bucket.from_bucket_name(self, id='LambdaResourcesBucket',
                                                                            bucket_name=f'{props.org}-{props.env}-lambda-resources'),
                                          key='workpay-payment-api-2020-07-26_22-10-19.zip'),
            handler='user_handler.create_user',
            role=lambda_full_access_role
        )

    @property
    def functions(self) -> Dict[LambdaFunction, _lambda.Function]:
        return {LambdaFunction.CREATE_USER: self.create_user_function}
