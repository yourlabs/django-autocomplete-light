# Django settings for test_project project.
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, 'fixtures'),
]

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'cities_light': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

SITE_ID = 1

STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^le6=#%$1z63o!#z^qr(r+^ix&iqx)@h*u$@8$bu&n8cv6m)go'

ROOT_URLCONF = 'test_project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'test_project.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'south',
    'cities_light',

    'autocomplete_light',
    'autocomplete_light.tests.apps.basic',
    'autocomplete_light.tests.apps.music',
    'autocomplete_light.tests.apps.autocomplete_test_case_app',
    'autocomplete_light.tests.apps.security_test',
    'autocomplete_light.tests.apps.dependant_autocomplete',
    'autocomplete_light.tests.apps.non_admin_add_another',

    'navigation_autocomplete',

    'django_jenkins',
)

try:
    import genericm2m
except ImportError:
    pass
else:
    INSTALLED_APPS += ('genericm2m',)

try:
    import taggit
except ImportError:
    pass
else:
    INSTALLED_APPS += ('taggit',)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'
