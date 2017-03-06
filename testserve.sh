#!/bin/bash
set -ex

# the directory of the script
# DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# the temp directory used, within $DIR
WORK_DIR=`mktemp -d`

# deletes the temp directory
function cleanup {
  rm -rf "$WORK_DIR"
  echo "Deleted temp working directory $WORK_DIR"
}

# register the cleanup function to be called on the EXIT signal
trap cleanup EXIT

export DJANGO_SETTINGS_MODULE="appliance_registry.settings_test"
export TEMP_DATABASE="$WORK_DIR/db.sqlite"

python manage.py migrate
python manage.py runserver 8003
