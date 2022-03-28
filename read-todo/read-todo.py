import boto3
import os

DYNAMODB_ENDPOINT_URL = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
client = boto3.client('dynamodb', endpoint_url= DYNAMODB_ENDPOINT_URL, region_name='eu-west-1')

def lambda_handler(event, context):
  """
  # Read todo lambda function
  Read todo lambda function to read record/records from DynamoDB table created usig Cloudformation. The function reads data
  from DynamoDB based on event of direct invokation. Three scenarios of event is possible,
  Event 1 => Reading all data (Scan) => {"UUID": "*"}
  Event 2 => Reading particular data (Get) => {"UUID": "UUID-1"}
  Event 3 => Reading record not existing in DynamoDB (Invalid) => {"UUID": "Invalid UUID"}
  """
  if "*" in event['UUID']:
    data = client.scan(TableName = 'Todo')
    return data['Items']
  else:
    data = client.get_item(
    TableName='Todo',
    Key={
        'UUID': {
          'S': event['UUID']
        }
    }
    )
    if "Item" not in data.keys():
      return "Opps, No such record in DynamoDB!!"
    else:
      return data['Item']