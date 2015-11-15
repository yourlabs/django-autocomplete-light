# Django settings for test_project project.
import os.path
import django

DEBUG = os.environ.get('DEBUG', False)
TEMPLATE_DEBUG = DEBUG
LOG_LEVEL = os.environ.get('DJANGO_LOG_LEVEL', 'INFO')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

LOG_DIR = os.environ.get('OPENSHIFT_LOG_DIR', 'log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

PUBLIC_DIR = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR', ''), 'wsgi/static')


DATABASES = {
    'default': {
        'NAME': os.environ.get('DJANGO_DATABASE_DEFAULT_NAME', 'db.sqlite'),
        'USER': os.environ.get('DJANGO_DATABASE_DEFAULT_USER', ''),
        'PASSWORD': os.environ.get('DJANGO_DATABASE_DEFAULT_PASSWORD', ''),
        'HOST': os.environ.get('DJANGO_DATABASE_DEFAULT_HOST', ''),
        'PORT': os.environ.get('DJANGO_DATABASE_DEFAULT_PORT', ''),
        'ENGINE': os.environ.get('DJANGO_DATABASE_DEFAULT_ENGINE',
            'django.db.backends.sqlite3'),

    }
}

if 'OPENSHIFT_DATA_DIR' in os.environ:
    DATABASES['default']['NAME'] = os.path.join(DATA_DIR, 'db.sqlite')

if 'OPENSHIFT_POSTGRESQL_DB_HOST' in os.environ:
    DATABASES['default']['NAME'] = os.environ['OPENSHIFT_APP_NAME']
    DATABASES['default']['USER'] = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
    DATABASES['default']['PASSWORD'] = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']
    DATABASES['default']['HOST'] = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
    DATABASES['default']['PORT'] = os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, 'fixtures'),
]

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
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
from socket import gethostname
ALLOWED_HOSTS = [
    gethostname(),
]

DNS = os.environ.get('OPENSHIFT_APP_DNS', None),
if DNS:
    ALLOWED_HOSTS += DNS

SITE_ID = 1

STATIC_URL = '/public/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')

if DATA_DIR:
    MEDIA_URL = '/static/media/'
    MEDIA_ROOT = os.path.join(DATA_DIR, 'media')

if PUBLIC_DIR:
    STATIC_URL = '/static/collected/'
    STATIC_ROOT = os.path.join(PUBLIC_DIR, 'collected')

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^le6=#%$1z63o!#z^qr(r+^ix&iqx)@h*u$@8$bu&n8cv6m)go'

ROOT_URLCONF = 'test_project.urls'

if django.VERSION < (1, 8):
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages'
    )
else:
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.template.context_processors.debug',
        'django.template.context_processors.i18n',
        'django.template.context_processors.media',
        'django.template.context_processors.static',
        'django.template.context_processors.tz',
        'django.contrib.messages.context_processors.messages'
    )



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
        },
        'DIRS': TEMPLATE_DIRS,
    },
]

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'test_project.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'autocomplete_light',
    'django.contrib.admin',
    'cities_light',

    'autocomplete_light.example_apps.basic',
    'autocomplete_light.example_apps.music',
    'autocomplete_light.example_apps.autocomplete_test_case_app',
    'autocomplete_light.example_apps.security_test',
    'autocomplete_light.example_apps.dependant_autocomplete',
    'autocomplete_light.example_apps.non_admin_add_another',
    'autocomplete_light.example_apps.create_choice_on_the_fly',

    'navigation_autocomplete',
    'admin_autocomplete_in_row',
    'bootstrap_modal'
)


if django.VERSION < (1, 7):
    INSTALLED_APPS += ('south',)
elif django.VERSION >= (1, 7):
    INSTALLED_APPS += (
        'autocomplete_light.example_apps.app_config_with_registry_file',
        'autocomplete_light.example_apps.app_config_without_registry_file.apps.AppConfigWithoutRegistryFile',
    )

if django.VERSION >= (1, 5):
    INSTALLED_APPS += (
        'autocomplete_light.example_apps.unuseable_virtualfield',
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

SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
    'cities_light': 'cities_light.south_migrations',
    'admin_autocomplete_in_row': 'ignore',
}
