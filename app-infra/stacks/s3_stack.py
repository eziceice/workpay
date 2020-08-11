from aws_cdk import (
    core,
    aws_s3 as s3
)

import stacks.properties as props


class S3Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        s3.Bucket(self, id='LambdaPythonResources', bucket_name=f'{props.org}-python-lambda-resources')
        s3.Bucket(self, id='LambdaJSResources', bucket_name=f'{props.org}-js-lambda-resources')

