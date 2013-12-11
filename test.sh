#!/bin/bash

set -x

WORKSPACE="${WORKSPACE:-$(pwd)}"
CLEAN_VIRTUALENV="${CLEAN_VIRTUALENV:-0}"
DJANGO_TAGGIT="${DJANGO_TAGGIT:-1}"
DJANGO_GENERIC_M2M="${DJANGO_GENERIC_M2M:-1}"
PYTHON_VERSION="${PYTHON_VERSION:-3.3}"
DJANGO_VERSION="${DJANGO_VERSION:-1.5}"

# Make a unique env path for this configuration
ENV_PATH="/tmp/autocomplete-light-test-$PYTHON_VERSION-$DJANGO_VERSION-$DJANGO_TAGGIT-$DJANGO_GENERIC_M2M"

# Get real django version
[ ! -d /tmp/django ] && git clone http://github.com/django/django.git $WORKSPACE/.django
cd $WORKSPACE/.django
git fetch --tags
DJANGO_VERSION=$(git tag -l | grep -E "$DJANGO_VERSION(\.[0-9])?$" | tail -n1)

# Clean virtualenv if necessary
[ "$CLEAN_VIRTUALENV" = "1" ] && rm -rf $ENV_PATH

# Make virtualenv if necessary
[ ! -d "$ENV_PATH" ] && virtualenv-$PYTHON_VERSION $ENV_PATH

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

$ENV_PATH/bin/pip install -e $WORKSPACE
$ENV_PATH/bin/pip install -Ur $WORKSPACE/test_project/requirements.txt
$ENV_PATH/bin/pip install -Ur $WORKSPACE/test_project/test_requirements.txt

# Install appropriate django version
$ENV_PATH/bin/pip install -U django==$DJANGO_VERSION

$ENV_PATH/bin/python $WORKSPACE/test_project/manage.py jenkins autocomplete_light
