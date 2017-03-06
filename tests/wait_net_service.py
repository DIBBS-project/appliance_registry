#!/usr/bin/env python
import argparse
import sys

from helpers import wait_net_service


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(description='Wait for a service to come up')
    parser.add_argument('-H', '--host', type=str, help="Host name", default='127.0.0.1')
    parser.add_argument('-p', '--port', type=int, help="Port", default=8000)
    parser.add_argument('-t', '--timeout', type=float, help="Timeout", default=10)
    args = parser.parse_args(argv[1:])

    if args.timeout <= 0:
        timeout = None
    else:
        timeout = args.timeout

    try:
        wait_net_service(args.host, args.port, timeout)
    except RuntimeError as e:
        if 'timed' not in str(e):
            raise
        print('timed out waiting for {}:{}'.format(args.host, args.port),
              file=sys.stderr)
        return -1

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
