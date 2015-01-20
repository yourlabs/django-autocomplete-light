#!/bin/bash

# Enable tracing (display executed lines)
set -x
# Halt on error!
set -e

WORKSPACE="${WORKSPACE:-$(pwd)}"
CLEAN_VIRTUALENV="${CLEAN_VIRTUALENV:-0}"
DJANGO_TAGGIT="${DJANGO_TAGGIT:-1}"
DJANGO_GENERIC_M2M="${DJANGO_GENERIC_M2M:-1}"
PYTHON_VERSION="${PYTHON_VERSION:-3.4}"
DJANGO_VERSION="${DJANGO_VERSION:-1.7}"
# for debug, it could be -e /dev/stdout
XVFB_FLAGS="${XVFB_FLAGS:-}"

# Make a unique env path for this configuration
ENV_PATH="$WORKSPACE/test_env"

# Get real django version
case "$DJANGO_VERSION" in
    1.4) django_dep='django>=1.4,<1.5' ;;
    1.5) django_dep='django>=1.5,<1.6' ;;
    1.6) django_dep='django>=1.6,<1.7' ;;
    1.7) django_dep='django>=1.7,<1.8' ;;
    *)   django_dep="django==$DJANGO_VERSION" ;;
esac

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

pip install $django_dep
pip install $DJANGO_TAGGIT $DJANGO_GENERIC_M2M \
    -e $WORKSPACE \
    -r $WORKSPACE/test_project/test_requirements.txt

cd $WORKSPACE
# NOTE: pg_virtualenv sets PGDATABASE, PGUSER, PGPASSWORD, PGHOST, PGPORT
if hash pg_virtualenv 2>/dev/null; then
    PG_VIRTUALENV=pg_virtualenv
fi

$PG_VIRTUALENV xvfb-run -a $XVFB_FLAGS test_project/manage.py test autocomplete_light --noinput --liveserver=localhost:9000-9200 --settings=test_project.settings_postgres

RET="$?"

exit $RET
