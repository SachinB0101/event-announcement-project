import json
import boto3
from botocore.exceptions import ClientError
import uuid
from datetime import datetime
import time

# AWS clients
s3 = boto3.client('s3')
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

# Configuration - UPDATE THESE VALUES
bucket_name = 'event-announcement-bucket-sachin'
events_file_key = 'events.json'
sns_topic_arn = 'arn:aws:sns:ca-central-1:231298815757:EventAnnouncements'
dynamodb_table_name = 'events' 
table_region = 'ca-central-1'

# Initialize DynamoDB table
table = dynamodb.Table(dynamodb_table_name)

def lambda_handler(event, context):
    try:
        # Set expiry 2 days (172800 seconds) from now
        expiry_time = int(time.time()) + 172800  

        new_event = json.loads(event['body'])  # Parse event body
        
        # Generate unique ID and timestamps for DynamoDB
        event_id = str(uuid.uuid4())
        
        # Prepare DynamoDB item
        dynamo_item = {
            'eventId': event_id,
            'title': new_event.get('title'),
            'date': new_event.get('date'),
            'description': new_event.get('description'),
            'expiresAt': expiry_time  # TTL attribute
        }
        
        # 1. Store in DynamoDB
        table.put_item(Item=dynamo_item)
        
        # 2. Update S3 (your existing functionality)
        try:
            response = s3.get_object(Bucket=bucket_name, Key=events_file_key)
            events_data = json.loads(response['Body'].read().decode('utf-8'))
            events_data.append(new_event)
            
            s3.put_object(
                Bucket=bucket_name,
                Key=events_file_key,
                Body=json.dumps(events_data, indent=2),
                ContentType='application/json'
            )
        except ClientError as e:
            print(f"S3 Error (non-critical): {e}")
            # Continue even if S3 update fails
        
        # 3. Send SNS notification
        message = f"New Event: {new_event['title']} on {new_event['date']}\n{new_event['description']}"
        sns.publish(TopicArn=sns_topic_arn, Message=message, Subject="New Event Announcement")
        
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, POST",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            'body': json.dumps({
                'message': f'Event created successfully! It will delete after {expiry_time}',
                'eventId': event_id  # Return the DynamoDB ID
            })
        }
    
    except ClientError as e:
        print(f"AWS Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, POST",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            'body': json.dumps({'message': 'Error processing the event'})
        }
    
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, POST",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            'body': json.dumps({'message': 'Unexpected error occurred'})
        }