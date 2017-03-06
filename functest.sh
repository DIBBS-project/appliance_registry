#!/bin/bash
set -e
# set -ex

# the directory of the script
# DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# the temp directory used, within $DIR
WORK_DIR=`mktemp -d`

if hash pyenv 2>/dev/null; then
    PYTHON=`pyenv which python`
    UWSGI=`pyenv which uwsgi`
else
    PYTHON=`which python`
    UWSGI=`which uwsgi`
fi

# deletes the temp directory
function cleanup {
  # pkill -P $$
  $UWSGI --stop "$WORK_DIR/uwsgi.pid"
  killall INT uwsgi
  # kill $RUNSERVER_ID
  rm -rf "$WORK_DIR"
  echo "Deleted temp working directory $WORK_DIR"
}

# register the cleanup function to be called on the EXIT signal
trap cleanup EXIT

export DJANGO_SETTINGS_MODULE="appliance_registry.settings_test"
export TEMP_DATABASE="$WORK_DIR/db.sqlite"

$PYTHON manage.py migrate
# $PYTHON manage.py runserver 8003 &
$UWSGI --http :8003 --module appliance_registry.wsgi --pidfile "$WORK_DIR/uwsgi.pid" &
# RUNSERVER_ID=$!
# echo $RUNSERVER_ID

# sleep 5
python tests/wait_net_service.py -p 8003

echo -e "\n == Django running ==\n"

$PYTHON tests/functional_tests.py
