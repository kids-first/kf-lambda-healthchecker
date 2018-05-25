import time
import logging
from botocore.vendored import requests


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handler(event, context):
    """
    Entry point to the lambda function
    """
    SERVICE = event['service']
    ENDPOINT = event['endpoint']

    t0 = time.time()
    resp = requests.get(SERVICE+ENDPOINT)
    t1 = time.time()

    code = resp.status_code

    logger.info('{} {} {} {}'.format(SERVICE, ENDPOINT, code, t1-t0))


if __name__ == '__main__':
    handler({'service': 'http://google.com', 'endpoint': '/'}, {})
