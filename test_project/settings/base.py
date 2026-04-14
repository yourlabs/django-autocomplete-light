import os
import sys

# hack for pytest:
sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), '..', '..'))

DEBUG = os.environ.get('DEBUG', False)

if 'DEBUG' not in os.environ:
    for cmd in ('runserver', 'pytest', 'py.test'):
        if cmd in sys.argv[0] or len(sys.argv) > 1 and cmd in sys.argv[1]:
            DEBUG = True
            continue

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


INSTALLED_APPS = [
    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # test apps
    'select2_foreign_key',
    'select2_list',
    'select2_generic_foreign_key',
    'select2_many_to_many',
    'select2_one_to_one',
    'select2_outside_admin',
    'select2_nestedadmin',
    'secure_data',
    'linked_data',
    'rename_forward',
    'forward_different_fields',
    'custom_select2',
    'select2_djhacker_formfield',

    # unit test app
    'tests',

    # Autocomplete
    'dal',
    'dal_select2',
    'queryset_sequence',
    'dal_queryset_sequence',
    'select2_taggit',
    'taggit',
    'nested_admin',

    # Project apps
    'django_extensions',
    'django.contrib.admin',
]

DATABASES = get_databases(BASE_DIR)

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

SECRET_KEY = '58$1jvc332=lyfk_m^jl6ody$7pbk18nm95==!r$7m5!2dp%l@'
ALLOWED_HOSTS = ['*']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_PASSWORD_VALIDATORS = []
DJANGO_LIVE_TEST_SERVER_ADDRESS = "localhost:8000-8010,8080,9200-9300"

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

SITE_ID = 1

STATIC_URL = '/public/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')

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
INTERNAL_IPS = ('127.0.0.1',)
