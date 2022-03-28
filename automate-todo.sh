#!/bin/bash

prettier="printf '\n'; printf -- '~%.0s' {1..210}; printf '\n'"

echo "Starting up docker localstack container in detached mode 🐳..."
docker run --rm -itd --name localstack -p 4566:4566 -p 4571:4571 localstack/localstack
eval $prettier

echo "Setting test AWS profile for localstack..."
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=eu-west-1
printenv |grep AWS_.*=
eval $prettier

echo "Creating zip of create-todo and read-todo before uplaoding to S3..."
python create-zip.py
eval $prettier

echo "Creating a s3 bucket named lambda-zip-bucket to store zip of todos lambdas..."
aws s3api create-bucket --bucket lambda-zip-bucket --endpoint-url=http://localhost:4566
eval $prettier

echo "Uploading todos lambdas zip to s3..."
aws s3 cp ./zipped/ s3://lambda-zip-bucket/ --recursive --endpoint-url=http://localhost:4566
eval $prettier

echo "Deploying Cloudformation stack to create DynamoDB and TODOs lambdas..."
aws cloudformation deploy --stack-name todo-stack --template-file "./stack.yaml" --endpoint-url=http://localhost:4566
eval $prettier

echo 'Invoking create-todo lambda to store {"title":"Test 1", "task":"Test 1 Lambda"} todo in DynamoDB Table...'
aws lambda invoke --function-name create-todo --cli-binary-format raw-in-base64-out --payload file://events/create1.txt output.txt --endpoint-url=http://localhost:4566
eval $prettier

echo 'Invoking create-todo lambda to store {"title":"Test 2", "task":"Test 2 Lambda"} todo in DynamoDB Table...'
aws lambda invoke --function-name create-todo --cli-binary-format raw-in-base64-out --payload file://events/create2.txt output.txt --endpoint-url=http://localhost:4566
eval $prettier

echo "The contents of DynamoDB table are..."
aws dynamodb scan --table-name Todo --endpoint-url=http://localhost:4566
eval $prettier

echo "Invoking read-todo lambda to fetch all data inside DynamoDB Table..."
aws lambda invoke --function-name read-todo --cli-binary-format raw-in-base64-out --payload file://events/read_all.txt output.txt --endpoint-url=http://localhost:4566 && cat output.txt
eval $prettier

echo "Invoking read-todo lambda to fetch Test 1 data inside DynamoDB Table..."
aws lambda invoke --function-name read-todo --cli-binary-format raw-in-base64-out --payload file://events/read_specific.txt output.txt --endpoint-url=http://localhost:4566 && cat output.txt
eval $prettier

echo "Invoking read-todo lambda with false event..."
aws lambda invoke --function-name read-todo --cli-binary-format raw-in-base64-out --payload file://events/read_invalid.txt output.txt --endpoint-url=http://localhost:4566 && cat output.txt
eval $prettier

echo "Shutting down localstack container 🐳..."
docker container stop localstack
eval $prettier