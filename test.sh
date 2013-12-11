#!/bin/bash

set -x

WORKSPACE="${WORKSPACE:-$(pwd)}"
CLEAN_VIRTUALENV="${CLEAN_VIRTUALENV:-0}"
DJANGO_TAGGIT="${DJANGO_TAGGIT:-1}"
DJANGO_GENERIC_M2M="${DJANGO_GENERIC_M2M:-1}"
PYTHON_VERSION="${PYTHON_VERSION:-3.3}"
DJANGO_VERSION="${DJANGO_VERSION:-1.5}"
JOB_UNIQUE_ID="$PYTHON_VERSION-$DJANGO_VERSION-$DJANGO_TAGGIT-$DJANGO_GENERIC_M2M"
export DATABASE_NAME="autocomplete_light_test_${JOB_UNIQUE_ID//[.-]}"

# Make a unique env path for this configuration
ENV_PATH="$WORKSPACE/test_env"

psql -c "drop database if exists $DATABASE_NAME;" -U postgres
psql -c "create database $DATABASE_NAME;" -U postgres

# Get real django version
[ ! -d "$HOME/django" ] && git clone http://github.com/django/django.git $HOME/.django
cd $HOME/.django
git fetch --tags
DJANGO_VERSION=$(git tag -l | grep -E "$DJANGO_VERSION(\.[0-9])?$" | tail -n1)

# Clean virtualenv if necessary
[ "$CLEAN_VIRTUALENV" = "1" ] && rm -rf $ENV_PATH

# Make virtualenv if necessary
[ ! -d "$ENV_PATH" ] && virtualenv-$PYTHON_VERSION $ENV_PATH

# Shebangs are too long without this and the kernel truncates them at 127
# characters.
virtualenv-$PYTHON_VERSION --relocatable $ENV_PATH

source $ENV_PATH/bin/activate

if [ "$DJANGO_TAGGIT" = "1" ]; then
    pip install -U django-taggit
else
    pip uninstall -y django-taggit
fi

if [ "$DJANGO_GENERIC_M2M" = "1" ]; then
    pip install -U django-generic-m2m
else
    pip uninstall -y django-generic-m2m
fi

pip install -e $WORKSPACE
pip install -Ur $WORKSPACE/test_project/requirements.txt
pip install -Ur $WORKSPACE/test_project/test_requirements.txt

# Install appropriate django version because other package upgrades like
# pip install -U django-jenkins has caused installation of the latest django 
# release because it requires django>=1.4.
pip install -U django==$DJANGO_VERSION

cd $WORKSPACE
test_project/manage.py jenkins autocomplete_light --liveserver=localhost:9000-9200 --settings=test_project.settings_postgres
