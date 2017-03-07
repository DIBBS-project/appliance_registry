#!/usr/bin/env python
"""
Test the Django service
"""
import argparse
import contextlib
import errno
import pathlib
import socket
import subprocess
import sys
import threading
import time

import requests

from common_dibbs.names import AUTHORIZATION_HEADER

from sham_cas import app as sham_cas
from helpers import DjangoRunserverManager, FlaskAppManager

TEST_DIR = pathlib.Path(__file__).resolve().parent
BASE_DIR = TEST_DIR.parent
MANAGE_PY = BASE_DIR / 'manage.py'


def assertStatus(response, expected, message=None):
    try:
        start, stop = expected
    except TypeError:
        if response.status_code == expected:
            return
    else:
        if start <= response.status_code < stop:
            return
        expected = '[{}, {})'.format(start, stop)

    if message:
        print(message, file=sys.stderr)

    print('Received status {}, expected {}\n-------------\n{}'
        .format(response.status_code, expected, response.content),
        file=sys.stderr)

    raise AssertionError(message or "bad status code")


def test():
    requests.get('http://localhost:7000/auth/tokens',
        headers={AUTHORIZATION_HEADER: 'alice,0'}
    )

    ROOT = 'http://localhost:8003'
    # sanity check root
    response = requests.get(ROOT)
    assertStatus(response, 200)

    alice_valid = {AUTHORIZATION_HEADER: 'alice,1'}
    alice_invalid = {AUTHORIZATION_HEADER: 'alice,0'}

    # check with auth
    response = requests.get(ROOT, headers=alice_valid)
    assertStatus(response, 200)

    # generic invalid token auth
    response = requests.get(ROOT, headers=alice_invalid)
    assertStatus(response, 403)

    site = {'name': 'chi-tacc', 'type': 'openstack', 'api_url': 'http://example.org/'}

    # refuse creation if anon
    response = requests.post(ROOT + '/sites/', json=site)
    assertStatus(response, 403, 'anon creation -> 403 UNAUTHORIZED')

    # refuse creation if bad token
    response = requests.post(ROOT + '/sites/', headers=alice_invalid, json=site)
    assertStatus(response, 403, 'bad token create -> 403 UNAUTHORIZED')

    # create site
    response = requests.post(ROOT + '/sites/', headers=alice_valid, json=site)
    assertStatus(response, 201, 'create site -> 201 CREATED')

    # refuse if duplicate name
    response = requests.post(ROOT + '/sites/', headers=alice_valid, json=site)
    # assertStatus(response, 409, 'create duplicate -> 409 CONFLICT')
    assertStatus(response, (400, 500), 'create duplicate -> 4xx error')

    response = requests.get(ROOT + '/appliances/')
    assertStatus(response, 200)

    response = requests.post(ROOT + '/appliances/', headers=alice_valid, json={
        'name': 'helloworld',
        'description': 'Prints "Hello, World!" for users to behold.',
    })
    assertStatus(response, 201)

    response = requests.post(ROOT + '/appliances/', headers=alice_valid, json={
        'name': 'helloworld',
        'description': 'dupe.',
    })
    assertStatus(response, (400, 500), 'create duplicate -> 4xx error')

    response = requests.post(ROOT + '/appliances/',
        json={'name': 'asdf', 'description': 'asdf'})
    assertStatus(response, 403, 'anon create should result in "unauthorized"')

    response = requests.get(ROOT + '/appliances/')
    assertStatus(response, 200)
    assert len(response.json()) == 1

    response = requests.get(ROOT + '/implementations/')
    assertStatus(response, 200)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args(argv[1:])

    # with DjangoRunserverManager(MANAGE_PY), FlaskAppManager(sham_cas, port=7000):
    with FlaskAppManager(sham_cas, port=7000): # launch django separately for now...
        result = test()

    return result

if __name__ == '__main__':
    sys.exit(main(sys.argv))
