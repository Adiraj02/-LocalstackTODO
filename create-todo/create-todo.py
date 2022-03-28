import boto3
import os

DYNAMODB_ENDPOINT_URL = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
client = boto3.client('dynamodb', endpoint_url= DYNAMODB_ENDPOINT_URL, region_name='eu-west-1')

def lambda_handler(event, context):
  """
  # Create todo lambda function
  Create todo lambda function to store file inside DynamoDB table created using Cloudformation. The function pushes data
  into DynamoDB based on the event passed from direct invokation in the form {"title":"Test 1", "task":"Test 1 Lambda"}
  where UUID is primary key of the DyanamoDB table assigned by auto incrementing the previous UUID. The UUID starts from
  UUID-1 and goes as long as records kept on adding.
  """
  UUID = ""
  list_uuid = []
  data = client.scan(TableName = 'Todo')
  available_records = data['Items']
  if len(available_records) == 0:
    UUID = "UUID-1"
  else:
    for record in available_records:
      list_uuid.append(record['UUID']['S'][-1])
    UUID = "UUID-" + str(int(max(list_uuid))+1)

  client.put_item(
    TableName='Todo',
    Item={
        'UUID':  {
          'S': UUID
        },
        'title': {
          'S': event['title']
        },
        'task': {
          'S': event['task']
        }
    }
  )