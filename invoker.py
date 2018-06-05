import copy
import os
import json
import boto3
from botocore.vendored import requests


endpoint_template = {
    "s3":{
        "service": "https://kf-api-dataservice.kids-first.io",
        "endpoint": "/status"
    }
}


function_arn = os.environ.get('FUNCTION', None)
env = os.environ.get('ENV', None)


def handler(event, context):
    """
    Invoke a function for each entry in endpoints.txt
    """
    endpoints = open('endpoints.txt').read()
    for line in endpoints.strip().split('\n'):
        service, endpoint = line.split(',')
        service = service.format(env=env)
        payload = {"service": service, "endpoint": endpoint}
        response = lam.invoke(
            FunctionName=function_arn,
            InvocationType='Event',
            Payload=str.encode(json.dumps(payload)),
        )
