import os
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

if 'OPENSHIFT_POSTGRESQL_DB_HOST' in os.environ:
    DATABASES['default']['NAME'] = os.environ['OPENSHIFT_APP_NAME']
    DATABASES['default']['USER'] = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
    DATABASES['default']['PASSWORD'] = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']
    DATABASES['default']['HOST'] = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
    DATABASES['default']['PORT'] = os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


def get_databases(base_dir):
    return {
        'default': {
            'ENGINE': os.environ.get('DJANGO_DB_ENGINE',
                'django.db.backends.sqlite3'),
            'NAME': os.environ.get('DJANGO_DB_NAME',
                os.path.join(base_dir, 'db.sqlite3')),
            'USER': os.environ.get('DJANGO_DB_USER', ''),
        }
    }


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # test apps
    'select2_foreign_key',
    'select2_generic_foreign_key',
    'select2_many_to_many',
    'select2_one_to_one',
    'select2_generic_m2m',
    'select2_taggit',
    'select2_tagging',
    'select2_outside_admin',
    'secure_data',
    'linked_data',

    # unit test app
    'tests',

    # Autocomplete
    'dal',
    # Enable plugins
    'dal_select2',
    'dal_queryset_sequence',

    # Project apps
    'django_extensions',
    'genericm2m',
    'tagging',
    'taggit',
]

if django.VERSION < (1, 10):
    # Doesn't support dj110
    # https://bitbucket.org/tkhyn/django-gm2m/issues/19
    INSTALLED_APPS += ['gm2m', 'select2_gm2m']

INSTALLED_APPS = INSTALLED_APPS + ['django.contrib.admin']

DATABASES = get_databases(BASE_DIR)

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

SECRET_KEY = '58$1jvc332=lyfk_m^jl6ody$7pbk18nm95==!r$7m5!2dp%l@'
DEBUG = True
ALLOWED_HOSTS = []

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_PASSWORD_VALIDATORS = []
DJANGO_LIVE_TEST_SERVER_ADDRESS="localhost:8000-8010,8080,9200-9300"

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DNS = os.environ.get('OPENSHIFT_APP_DNS', None),
if DNS:
    ALLOWED_HOSTS += DNS

SITE_ID = 1


from socket import gethostname
ALLOWED_HOSTS = [
    gethostname(),
]

STATIC_URL = '/public/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')

if DATA_DIR:
    MEDIA_URL = '/static/media/'
    MEDIA_ROOT = os.path.join(DATA_DIR, 'media')

if PUBLIC_DIR:
    STATIC_URL = '/static/collected/'
    STATIC_ROOT = os.path.join(PUBLIC_DIR, 'collected')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.join(PROJECT_ROOT, 'templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

SELENIUM_PAGE_LOAD_TIMEOUT = 100
SELENIUM_TIMEOUT = 100


