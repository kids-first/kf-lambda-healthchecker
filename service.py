import time
import logging
import boto3
from botocore.vendored import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event, context):
    """
    Entry point to the lambda function
    """
    SERVICE = event['service']
    ENDPOINT = event['endpoint']

    SERVICE = SERVICE.replace('-prd', '')

    t0 = time.time()
    headers = {'User-Agent': 'HealthChecker'}
    if '_checks' in ENDPOINT:
        resp = requests.post(SERVICE+ENDPOINT, headers=headers)
    else:
        resp = requests.get(SERVICE+ENDPOINT, headers=headers)
    t1 = time.time()

    code = resp.status_code

    # To stdout/cloudwatch log
    logger.info('{} {} {} {}'.format(SERVICE, ENDPOINT, code, t1-t0))
    metrics = [
        {
            'MetricName': 'ResponseTime'+ENDPOINT.replace('/',''),
            'Dimensions': [
                {
                    'Name': 'endpoint',
                    'Value': ENDPOINT
                },
                {
                    'Name': 'service',
                    'Value': SERVICE 
                }
            ],
            'Timestamp': time.time(),
            'Value': t1-t0,
            'Unit': 'Seconds'
        },
        {
            'MetricName': 'ErrorCount'+ENDPOINT.replace('/',''),
            'Dimensions': [
                {
                    'Name': 'endpoint',
                    'Value': ENDPOINT
                },
                {
                    'Name': 'service',
                    'Value': SERVICE 
                }
            ],
            'Timestamp': time.time(),
            'Value': 1 if code >= 400 else 0,
            'Unit': 'Count'
        }
    ]

    # To cloudwatch metric directly
    client = boto3.client('cloudwatch', region_name='us-east-1')
    response = client.put_metric_data(
	Namespace='HealthChecks',
	MetricData=metrics
    )
    return '{} {} {} {}'.format(SERVICE, ENDPOINT, code, t1-t0)
