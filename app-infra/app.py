#!/usr/bin/env python3

from aws_cdk import core

from stacks.lambda_stack import LambdaStack
from stacks.apigw_stack import APIGatewayStack
from stacks.dynamodb_stack import DynamoDBStack
from stacks.s3_stack import S3Stack
from stacks.pinpoint_stack import PinPointStack
import stacks.properties as props


app = core.App()

PinPointStack(app, f'{props.org}-{props.env}-pinpoint-stack')
lambda_stack = LambdaStack(app, f'{props.org}-{props.env}-lambda-stack')
APIGatewayStack(app, f'{props.org}-{props.env}-apigw-stack', functions=lambda_stack.functions)
DynamoDBStack(app, f'{props.org}-{props.env}-dynamodb-stack')
S3Stack(app, f'{props.org}-s3-stack')


app.synth()
