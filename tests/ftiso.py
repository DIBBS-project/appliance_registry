import multiprocessing
import os
import pathlib
import sys
import tempfile
import time
import threading

import django
from django.core.management import execute_from_command_line
import requests

from helpers import wait_net_service


def runserver(port):
    execute_from_command_line(])


def main(argv=None):
    sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
    port = 8003

    os.environ['DJANGO_SETTINGS_MODULE'] = 'appliance_registry.test_settings'
    with tempfile.TemporaryDirectory() as td:
        os.environ['TEMP_DATABASE'] = td + '/db.sqlite'
        print(td)
        django.setup()

        execute_from_command_line(['manage.py', 'migrate'])

        t = threading.Thread(
            target=execute_from_command_line,
            args=(['manage.py', 'runserver', str(port),),
            daemon=True,
        )
        t.start()
        wait_net_service('127.0.0.1', 8003, timeout=5)
        #
        print(requests.get('http://localhost:8003/').json())
        #
        time.sleep


if __name__ == '__main__':
    sys.exit(main(sys.argv))
