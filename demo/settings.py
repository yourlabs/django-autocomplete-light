import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)

# demo/ must be first so 'urls' and 'views' resolve here, not test_project/.
for p in (HERE, os.path.join(REPO_ROOT, 'src'), os.path.join(REPO_ROOT, 'test_project')):
    if p not in sys.path:
        sys.path.insert(0, p)

DEBUG = True
SECRET_KEY = 'dal-alight-demo-secret'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # DAL core + alight plugin only (no dal_select2)
    'dal',
    'dal_alight',
    # Demo apps (reused from test_project/)
    'alight_foreign_key',
    'alight_many_to_many',
    'alight_linked_data',
    'alight_list',
    'alight_tag',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(HERE, 'db.sqlite3'),
    }
}

ROOT_URLCONF = 'urls'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(HERE, 'templates')],
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

STATIC_URL = '/static/'

# Map the submodule's compiled JS/CSS to the dal_alight/ URL namespace so
# AlightWidgetMixin.media paths (dal_alight/autocomplete-light.{js,css}) resolve.
STATICFILES_DIRS = [
    ('dal_alight', os.path.join(
        REPO_ROOT, 'src', 'dal_alight', 'static', 'dal_alight',
        'autocomplete_light', 'static', 'autocomplete_light',
    )),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
