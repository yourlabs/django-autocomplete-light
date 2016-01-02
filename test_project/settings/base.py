import os
import django


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
    'select2_tagulous',
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
    'sbo_selenium',
    'genericm2m',
    'taggit',
    'tagulous',
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

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
