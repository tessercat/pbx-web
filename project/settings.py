""" Project settings module. """
import logging
import os
from project import env


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Django globals from env.

django_globals = env.get_settings(BASE_DIR, 'django_globals.py')

ADMINS = django_globals['ADMINS']

ALLOWED_HOSTS = django_globals['ALLOWED_HOSTS']

INSTALLED_APPS = django_globals['INSTALLED_APPS']

SECRET_KEY = env.get_secret_key(BASE_DIR)

SERVER_EMAIL = django_globals['SERVER_EMAIL']

TIME_ZONE = django_globals['TIME_ZONE']


# Custom globals from env.

PORTS = env.get_settings(BASE_DIR, 'ports.py')

PBX_HOSTNAME = django_globals['ALLOWED_HOSTS'][0]


# Other custom Django settings.

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
