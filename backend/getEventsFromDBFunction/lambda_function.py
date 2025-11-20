import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('events')

def lambda_handler(event, context):
    try:
        # Scan DynamoDB table to get all events
        response = table.scan()
        events = response.get('Items', [])

        # Remove 'expiresAt' from each item
        for item in events:
            if 'expiresAt' in item:
                del item['expiresAt']
        
        # Return events
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            'body': json.dumps(events)
        }
        
    except ClientError as e:
        print(f"AWS Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            'body': json.dumps({'error': 'Failed to fetch events'})
        }

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            'body': json.dumps({'message': 'Unexpected error occurred'})
        }