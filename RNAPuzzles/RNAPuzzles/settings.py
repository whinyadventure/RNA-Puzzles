"""
Django settings for RNAPuzzles project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm7$0i2x2oqv%#gi5!6j*&k^sg5@djo(2f0!j^#*upn!+v-k7vy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

LOGOUT_REDIRECT_URL = '/'
DOMAIN_URL = "127.0.0.1"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'martor',
    'crispy_forms',
    'guardian',
    'publications',
    'captcha',
    'tempus_dominus',
    'rnapuzzles',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTHENTICATION_BACKENDS = (

    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_NAME = "AnonymousUser@foo.foo"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rnapuzzles.middleware.request.GuardianAuthenticationMiddleware',
]

ROOT_URLCONF = 'RNAPuzzles.urls'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "rnapuzzles/templates")],
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

WSGI_APPLICATION = 'RNAPuzzles.wsgi.application'
AUTH_USER_MODEL = 'rnapuzzles.CustomUser'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rna',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-GB'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATETIME_FORMAT = 'd M Y, H:i '
DATETIME_INPUT_FORMATS = '%d-%m-%Y %H:%M'

TEMPUS_DOMINUS_LOCALIZE = True
TEMPUS_DOMINUS_INCLUDE_ASSETS = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_SUBMISSIONS = "submissions"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "rnapuzzles/static"),
)

# Global martor settings
# Input: string boolean, `true/false`
MARTOR_ENABLE_CONFIGS = {
    'imgur': 'true',     # to enable/disable imgur/custom uploader.
    'mention': 'false',  # to enable/disable mention
    'jquery': 'true',    # to include/revoke jquery (require for admin default django)
    'living': 'false',   # to enable/disable live updates in preview
    'spellcheck': 'false',
}

# To setup the martor editor with label or not (default is False)
MARTOR_ENABLE_LABEL = False

# Imgur API Keys
MARTOR_IMGUR_CLIENT_ID = 'your-client-id'
MARTOR_IMGUR_API_KEY = 'your-api-key'

# Safe Mode
MARTOR_MARKDOWN_SAFE_MODE = True # default

# Markdownify
MARTOR_MARKDOWNIFY_FUNCTION = 'martor.utils.markdownify' # default
MARTOR_MARKDOWNIFY_URL = '/martor/markdownify/' # default

# Markdown extensions (default)
MARTOR_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.smarty',
    'markdown.extensions.fenced_code',

    # Custom markdown extensions.
    'martor.extensions.urlize',
    'martor.extensions.del_ins',    # ~~strikethrough~~ and ++underscores++
    'martor.extensions.mention',    # to parse markdown mention
    'martor.extensions.emoji',      # to parse markdown emoji
    'martor.extensions.mdx_video',  # to parse embed/iframe video
]

# Markdown Extensions Configs
MARTOR_MARKDOWN_EXTENSION_CONFIGS = {}

# Markdown urls
MARTOR_UPLOAD_URL = '/martor/uploader/' # default
MARTOR_SEARCH_USERS_URL = '/martor/search-user/' # default

# Markdown Extensions
# MARTOR_MARKDOWN_BASE_EMOJI_URL = 'https://www.webfx.com/tools/emoji-cheat-sheet/graphics/emojis/'     # from webfx
MARTOR_MARKDOWN_BASE_EMOJI_URL = 'https://github.githubassets.com/images/icons/emoji/'                  # default from github
MARTOR_MARKDOWN_BASE_MENTION_URL = 'https://python.web.id/author/'

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']


# RabbitMq
CELERY_BROKER_URL = 'amqp://user:password@{host}:{port}'.format(
    host=os.getenv('RABBITMQ_HOST', 'localhost'),
    port=os.getenv('RABBITMQ_PORT', '5672')
)



CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
