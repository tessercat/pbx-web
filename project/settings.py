""" Project settings module. """
import ast
import os
import random
from common.registries import common_protected_paths_registry
from fsapi.registries import fsapi_handler_registry
from dialplan.registries import dialplan_handler_registry
from directory.registries import directory_handler_registry
from verto.registries import (
    verto_dialplan_handler_registry,
    verto_directory_handler_registry
)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Load SETTINGS from dict literal.
with open(os.path.join(BASE_DIR, 'var', 'settings.py')) as settings_fd:
    SETTINGS = ast.literal_eval(settings_fd.read())


# Load SECRET_KEY from file or write a new one.
SECRET_KEY_FILE = os.path.join(BASE_DIR, 'var', 'secret_key')
if os.path.isfile(SECRET_KEY_FILE):
    with open(SECRET_KEY_FILE) as secret_fd:
        SECRET_KEY = secret_fd.read().strip()
else:
    SECRET_KEY = ''.join(random.choice(
        'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    ) for _ in range(50))
    with open(SECRET_KEY_FILE, 'w') as secret_fd:
        secret_fd.write(SECRET_KEY)


# Required custom settings

ADMINS = SETTINGS['ADMINS']

FIREWALL_PORT = SETTINGS['FIREWALL_PORT']

PBX_HOSTNAME = SETTINGS['PBX_HOSTNAME']

RTP_PORT_START = SETTINGS['RTP_PORT_START']

RTP_PORT_END = SETTINGS['RTP_PORT_END']

SERVER_EMAIL = SETTINGS['SERVER_EMAIL']

STUN_PORT = SETTINGS['STUN_PORT']

TIME_ZONE = SETTINGS['TIME_ZONE']

VERTO_PORT = SETTINGS['VERTO_PORT']


# Other custom settings

ALLOWED_HOSTS = (
    PBX_HOSTNAME,
    'localhost',
)

CSRF_FAILURE_VIEW = 'common.views.custom403'

DEBUG = False

EMAIL_SUBJECT_PREFIX = '[PBX] '


# App-specific settings

COMMON_CSS = None

COMMON_PROTECTED_PATHS = common_protected_paths_registry

FSAPI_REQUEST_HANDLERS = fsapi_handler_registry

DIRECTORY_HANDLERS = directory_handler_registry

DIALPLAN_HANDLERS = dialplan_handler_registry

VERTO_DIRECTORY_HANDLERS = verto_directory_handler_registry

VERTO_DIALPLAN_HANDLERS = verto_dialplan_handler_registry

CONFERENCE_CSS = None

CONFERENCE_CLIENT_JS = None

CONFERENCE_ADAPTER_JS = None


# Header and cookie definition

# Assume no port in nginx HTTP-X-FORWARDED-HOST for CSRF match.
# https://stackoverflow.com/questions/27533011

CSRF_COOKIE_HTTPONLY = True

CSRF_COOKIE_SAMESITE = 'Strict'

CSRF_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SAMESITE = 'Strict'

SESSION_COOKIE_SECURE = True

USE_X_FORWARDED_HOST = True

USE_X_FORWARDED_PORT = True


# Application definition

INSTALLED_APPS = [
    'django_prometheus',
    'common.apps.CommonConfig',
    'fsapi.apps.FsapiConfig',
    'directory.apps.DirectoryConfig',
    'dialplan.apps.DialplanConfig',
    'verto.apps.VertoConfig',
    'conference.apps.ConferenceConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'common.middleware.ProtectedPathsMiddleware',
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'common.middleware.AdminKnockMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'var', 'db.sqlite3'),
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
