from botocore.vendored import requests


def handler(event, context):
    """
    Entry point to the lambda function
    """
    requests.get('http://kids-first.io')
