#!/bin/bash

# Enable tracing (display executed lines)
set -x
# Halt on error!
set -e

WORKSPACE="${WORKSPACE:-$(pwd)}"
CLEAN_VIRTUALENV="${CLEAN_VIRTUALENV:-0}"
DJANGO_TAGGIT="${DJANGO_TAGGIT:-1}"
DJANGO_GENERIC_M2M="${DJANGO_GENERIC_M2M:-1}"
PYTHON_VERSION="${PYTHON_VERSION:-3.3}"
DJANGO_VERSION="${DJANGO_VERSION:-1.6.1}"
# for debug, it could be -e /dev/stdout
XVFB_FLAGS="${XVFB_FLAGS:-}"

# Make a unique env path for this configuration
ENV_PATH="$WORKSPACE/test_env"

# Get real django version
[ "$DJANGO_VERSION" = "1.4" ] && DJANGO_VERSION="1.4.10"
[ "$DJANGO_VERSION" = "1.5" ] && DJANGO_VERSION="1.5.5"
[ "$DJANGO_VERSION" = "1.6" ] && DJANGO_VERSION="1.6.1"

# Clean virtualenv if necessary
[ "$CLEAN_VIRTUALENV" = "1" ] && rm -rf $ENV_PATH

# Make virtualenv if necessary
[ ! -d "$ENV_PATH" ] && virtualenv-$PYTHON_VERSION $ENV_PATH

# Shebangs are too long without this and the kernel truncates them at 127
# characters.
virtualenv-$PYTHON_VERSION --relocatable $ENV_PATH

source $ENV_PATH/bin/activate

[ "$DJANGO_TAGGIT" = "1" ] && DJANGO_TAGGIT=django-taggit || DJANGO_TAGGIT=""

[ "$DJANGO_GENERIC_M2M" = "1" ] && DJANGO_GENERIC_M2M=django-generic-m2m || DJANGO_GENERIC_M2M=""

# 2.1.7 has a bad migration
pip install django-cities-light==2.1.8
pip install $DJANGO_TAGGIT $DJANGO_GENERIC_M2M \
    -e $WORKSPACE \
    -r $WORKSPACE/test_project/test_requirements.txt \
    django==$DJANGO_VERSION

cd $WORKSPACE
# NOTE: pg_virtualenv sets PGDATABASE, PGUSER, PGPASSWORD, PGHOST, PGPORT
if hash pg_virtualenv 2>/dev/null; then
    PG_VIRTUALENV=pg_virtualenv
fi

$PG_VIRTUALENV xvfb-run -a $XVFB_FLAGS test_project/manage.py test autocomplete_light --noinput --liveserver=localhost:9000-9200 --settings=test_project.settings_postgres

RET="$?"

exit $RET
