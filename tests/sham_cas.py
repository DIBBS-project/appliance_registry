import contextlib
import json

from flask import Flask, request

from common_dibbs.names import AUTHORIZATION_HEADER

assert not AUTHORIZATION_HEADER.startswith('HTTP')

app = Flask(__name__)
# app.config['SERVER_NAME'] = 'localhost:7000'


@app.route('/')
def hello_world():
    return repr(dict(app.config))
    # return 'Hello, World!'


@app.route('/_shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


@app.route('/auth/tokens', methods=['GET'])
def validate_fake_token():
    try:
        username, valid = request.headers[AUTHORIZATION_HEADER].split(',')
    except KeyError:
        return json.dumps({'error': 'missing token'}), 400
    if int(valid):
        return json.dumps({'username': username}), 200
    else:
        return json.dumps({'error': 'unauthorized'}), 403


# @contextlib.contextmanager
# def sp_sham_cas():
#     subprocess.Popen([sys.executable, MANAGE_PY, 'runserver'])
#     sham_cas = subprocess.Popen(
#         [sys.executable, '-m', 'flask', 'run'],
#         env={
#             'FLASK_APP': str(TEST_DIR / 'sham_cas.py'),
#             'LC_ALL': 'en_US.UTF-8',
#             'LANG': 'en_US.UTF-8',
#         },
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         universal_newlines=True,
#     )
#     for line in sham_cas.stderr:
#         print(line)
#         if 'Running on' in line:
#             break
#
#     yield
#
#     sc_out, sc_err = sham_cas.communicate()
#     print(sc_out)
#     print(sc_err)
#
#     sham_cas.terminate()
#     sham_cas.wait(1)
