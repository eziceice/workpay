#!/usr/bin/env python3
from aws_cdk import (
    core,
    aws_dynamodb as dynamodb
)
from stacks import properties as props


class DynamoDBStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.create_user_table()

    def create_user_table(self):
        # create dynamo table
        request_table = dynamodb.Table(
            self, id="UserTable", table_name=f"{props.org}-{props.env}-user-table",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.RETAIN
        )
