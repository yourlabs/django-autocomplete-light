import os

from .settings import *

# NOTE: environment set by pg_virtualenv
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PGDATABASE', 'autocomplete_light_test'),
        'USER': os.environ.get('PGUSER', 'postgres'),
        'PASSWORD': os.environ.get('PGPASSWORD', ''),
        'HOST': os.environ.get('PGHOST', ''),
        'PORT': os.environ.get('PGPORT', ''),
    }
}


