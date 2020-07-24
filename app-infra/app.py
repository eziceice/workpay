#!/usr/bin/env python3

from aws_cdk import core

from stacks.lambda_stack import LambdaStack
from stacks.apigw_stack import APIGatewayStack
from stacks.dynamodb_stack import DynamoDBStack
import stacks.properties as props


app = core.App()

lambda_stack = LambdaStack(app, f"{props.org}-{props.env}-lambda-stack")
APIGatewayStack(app, f"{props.org}-{props.env}-apigw-stack", functions=lambda_stack.functions)
DynamoDBStack(app, f"{props.org}-{props.env}-dynamodb-stack")

app.synth()
