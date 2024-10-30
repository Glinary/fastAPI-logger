from dotenv import load_dotenv
import boto3
import os

load_dotenv()
REGION_NAME = os.getenv('REGION_NAME')
TABLE_NAME = os.getenv('TABLE_NAME')

class DynamoDBLogger:
    def __init__(self, region_name=REGION_NAME, table_name=TABLE_NAME):
        self.dynamodb = boto3.client('dynamodb', region_name=region_name)
        self.table_name = table_name

    def log_item(self, sender_id: str, timestamp: str = None, text: str = None, event_type: str = None):
        """
        Inserts an item into the DynamoDB table with a specified sender_id and timestamp.
        
        Args:
            sender_id (str): The partition key for the item.
            timestamp (str): The sort key for the item, defaults to current UTC time if not provided.
            event_type: (string) event type to identify whether it is a user or a bot
            message: (string) the logged message
        """
        # Construct item with partition and sort keys
        item = {
            'sender_id': {'S': sender_id},
            'timestamp': {'S': timestamp},
            'event_type': {'S': event_type},
            'message': {'S': text}
        }
        
        # Insert item into DynamoDB
        self.dynamodb.put_item(TableName=self.table_name, Item=item)
        print(f"Item logged with sender_id: {sender_id} and timestamp: {timestamp}")
