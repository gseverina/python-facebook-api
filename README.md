# build docker image
docker build -t python-facebook-api .

# Run and Test locally
docker run -p 9000:8080  python-facebook-api:latest
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"key": "value 1"}' .

# login (TODO: implement aws account id variable)
docker login -u AWS -p $(aws ecr get-login-password --profile admin --region us-east-1) 497599533144.dkr.ecr.us-east-1.amazonaws.com

# create de repository if not exists
aws ecr create-repository --repository-name python-facebook-api --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

# Tag the image (TODO: implement aws account id variable)
docker tag  python-facebook-api:latest 497599533144.dkr.ecr.us-east-1.amazonaws.com/python-facebook-api:latest

# push (TODO: implement aws account id variable)
docker push 497599533144.dkr.ecr.us-east-1.amazonaws.com/python-facebook-api:latest

# create the lambda function from AWS Console (TODO: implement create the lambda avoiding the aws console, like using aws-cli)
https://console.aws.amazon.com/lambda/home/functions

# invoke
aws lambda invoke --function-name python-facebook-api --payload '{"key": "value"}' out.json --profile admin

