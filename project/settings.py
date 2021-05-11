""" Project settings module. """
import ast
import os
import random


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

INTERCOM_PORTS = SETTINGS['INTERCOM_PORTS']


# Other custom settings

ALLOWED_HOSTS = (
    PBX_HOSTNAME,
    'localhost',
)

CSRF_FAILURE_VIEW = 'common.views.custom403'

DEBUG = False

EMAIL_SUBJECT_PREFIX = '[PBX] '


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
    'configuration.apps.ConfigurationConfig',
    'directory.apps.DirectoryConfig',
    'dialplan.apps.DialplanConfig',
    'sofia.apps.SofiaConfig',
    'verto.apps.VertoConfig',
    'action.apps.ActionConfig',
    'call.apps.CallConfig',
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
