import os
from pathlib import Path

from dotenv import load_dotenv

DEBUG = True

load_dotenv()

SECRET_KEY = str(os.getenv('SECRET_KEY'))
BIG_BOSS_ID = os.getenv('BIG_BOSS_ID')
REGBOT_TOKEN = str(os.getenv('REGBOT_TOKEN'))

BASE_URL = 'http://127.0.0.1:8443'
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = [
    '3e68-95-72-155-198.eu.ngrok.io',
    '127.0.0.1',
    '127.0.0.1:8000',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': str(os.getenv('BD_NAME')),
        'USER': str(os.getenv('BD_USER')),
        'PASSWORD': str(os.getenv('BD_PASSWORD')),
        'HOST': str(os.getenv('BD_HOST')),
        'PORT': '3306',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bots',
    'login',
    'plans',
    'groups',
    'rest_framework',
    'kr',
    'core',
    'message',
    'works',
    # 'quizzes',
    'edubot.apps.EdubotConfig',
    'regbot.apps.RegbotConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middlewares.is_admin',
    'core.middlewares.is_admin_bot',
    'core.middlewares.is_yours',
]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

ROOT_URLCONF = 'botproject.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'context_processors.conproc.get_bot',
                'context_processors.conproc.get_plan',
                'context_processors.conproc.get_admin',
                'context_processors.conproc.get_group',
                'context_processors.conproc.get_kr',
                'context_processors.conproc.get_crumbs',
            ],
            'libraries': {
                'custom_tags': 'core.custom_tags'
            }
        },
    },
]

WSGI_APPLICATION = 'botproject.wsgi.application'

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMP_URL = f'{MEDIA_URL}temp/'
TEMP_ROOT = os.path.join(MEDIA_ROOT, 'temp')
