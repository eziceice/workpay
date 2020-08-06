from typing import Dict

from aws_cdk import (
    core,
    aws_pinpoint as pinpoint
)

import stacks.properties as props


class PinPointStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        app = pinpoint.CfnApp(self, id='PinPointService', name=f'{props.org}-{props.env}-pinpoint')
        pinpoint.CfnSMSChannel(self, id='SMSChannel', application_id=app.ref, enabled=True, sender_id='WorkPay')
        core.CfnOutput(self, id='PinPointAppId', value=app.ref)
