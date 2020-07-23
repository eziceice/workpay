import json
import boto3


def create_user(event, context):
    body = json.loads(event["body"])
    user_id = event["requestContext"]["requestId"]
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("workpay-test-user-table")
    table.put_item(
        Item={
            "id": user_id,
            "name": body["name"],
            "email": body["email"],
            "phone": body["phone"]
        }
    )
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': 'User has been created successfully'})
    }