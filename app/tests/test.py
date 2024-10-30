import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('aiip_webhook_logging')

table.put_item(Item={
    'sender_id': '1231234',
    'timestamp': '1231234',
    'test': '1231234',
    'event_type': "event"
})