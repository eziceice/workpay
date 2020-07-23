from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_iam as iam
)

import stacks.properties as props


class LambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_full_access_role = iam.Role(self, id="LambdaFullAccessRole",
                                           role_name=f"{props.owner}-{props.env}-lambda-full-access-role",
                                           assumed_by=iam.ServicePrincipal(
                                               "lambda.amazonaws.com", region=props.aws_region),
                                           managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                                               "AWSLambdaFullAccess")])

        _lambda.Function(
            self, id="CreateUserFunction",
            function_name=f"{props.owner}-{props.env}-create-user-function",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset(path="../app"),
            handler="user_handler.create_user",
            role=lambda_full_access_role
        )

        # self.method_not_supported_handler.add_permission(id='ApiGatewayInvokePermission',
        #                                                  principal=iam.ServicePrincipal(
        #                                                      'apigateway.amazonaws.com', region=props.aws_region),
        #                                                  action='lambda:*')
