# -*- coding: utf-8 -*-
import pytest

from optimus.exceptions import InvalidHostname
from optimus.utils import get_host_parts


@pytest.mark.parametrize('hostname,ip,port', [
    (
        '',
        '127.0.0.1',
        80,
    ),
    (
        '0.0.0.0',
        '0.0.0.0',
        80,
    ),
    (
        'localhost',
        'localhost',
        80,
    ),
    (
        '0.0.0.0:8001',
        '0.0.0.0',
        8001,
    ),
    (
        'localhost:8001',
        'localhost',
        8001,
    ),
])
def test_valid_hostname(hostname, ip, port):
    """
    Testing hostname arg validation on correct value
    """

    assert get_host_parts(hostname) == (ip, port)


@pytest.mark.parametrize('hostname', [
    ':8001',
    '::8001',
    '2000:8001:80',
    '0.0.0.0:',
    '0.0.0.0:foo',
])
def test_invalid_hostname(hostname):
    """
    Testing hostname arg validation on correct value
    """

    with pytest.raises(InvalidHostname):
        get_host_parts(hostname)
