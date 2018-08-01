import pytest
import service
from mock import patch, Mock
from moto import mock_cloudwatch


@mock_cloudwatch
def test_handler():
    """
    Test the service handler
    """
    r_patch = patch('service.requests')
    r_mock = r_patch.start()
    mock_resp = Mock()
    mock_resp.status_code = 200
    r_mock.get.return_value = mock_resp

    event = {
        'service': 'http://kids-first.github.io',
        'endpoint': '/'
    }
    service.handler(event, {})

    assert r_mock.get.call_count == 1
    r_mock.get.assert_called_with('http://kids-first.github.io/',
                                  headers={'User-Agent': 'HealthChecker'})


@mock_cloudwatch
def test_bad_status():
    """
    Test bad status code
    """
    r_patch = patch('service.requests')
    r_mock = r_patch.start()
    mock_resp = Mock()
    mock_resp.status_code = 200
    r_mock.get.return_value = mock_resp

    event = {
        'service': 'http://kids-first.github.io',
        'endpoint': '/'
    }
    service.handler(event, {})

    assert r_mock.get.call_count == 1
    r_mock.get.assert_called_with('http://kids-first.github.io/',
                                  headers={'User-Agent': 'HealthChecker'})
