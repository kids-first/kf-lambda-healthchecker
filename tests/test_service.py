import pytest
import service
from mock import patch


def test_handler():
    """
    Test the service handler
    """
    r_patch = patch('service.requests')
    r_mock = r_patch.start()

    event = {
        'service': 'http://kids-first.github.io',
        'endpoint': '/'
    }
    service.handler(event, {})

    assert r_mock.get.call_count == 1
    r_mock.get.assert_called_with('http://kids-first.github.io/')
