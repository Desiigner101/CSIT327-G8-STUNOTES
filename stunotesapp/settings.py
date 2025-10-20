"""
Django settings for stunotes project.
Optimized for deployment on Vercel using Supabase PostgreSQL.
"""

import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
from decouple import config

# Load environment variables
load_dotenv()

# ---------------------------------------------------
# BASE DIRECTORY
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------
# SECURITY SETTINGS
# ---------------------------------------------------
SECRET_KEY = config('SECRET_KEY', default='django-insecure-placeholder')
DEBUG = config('DEBUG', default=False, cast=bool)

# Allow multiple domains (Vercel, localhost)
raw_allowed = config('ALLOWED_HOSTS', default='.vercel.app,localhost,127.0.0.1')
ALLOWED_HOSTS = [h.strip() for h in raw_allowed.split(',') if h.strip()]


# ---------------------------------------------------
# APPLICATIONS
# ---------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files on Vercel
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stunotesapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # global templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'stunotesapp.wsgi.application'


# ---------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------
# Priority:
# 1. DATABASE_URL (Supabase connection string)
# 2. Individual DB_* environment variables
# 3. SQLite fallback (local use only)
database_url = config('DATABASE_URL', default='')

if database_url:
    DATABASES = {
        'default': dj_database_url.parse(database_url, conn_max_age=0)
    }
    DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}
else:
    db_engine = config('DB_ENGINE', default='')
    if db_engine:
        DATABASES = {
            'default': {
                'ENGINE': db_engine,
                'HOST': config('DB_HOST', default=''),
                'NAME': config('DB_NAME', default=''),
                'USER': config('DB_USER', default=''),
                'PASSWORD': config('DB_PASSWORD', default=''),
                'PORT': config('DB_PORT', default=''),
                'OPTIONS': {'sslmode': 'require'},
                'CONN_MAX_AGE': 0,
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }


# ---------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------
AUTH_USER_MODEL = 'notes.User'
LOGIN_URL = 'notes:login'


# ---------------------------------------------------
# STATIC & MEDIA FILES
# ---------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # for Vercel deployment

# Static files config - Use simple storage for development
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage' if DEBUG else 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configure WhiteNoise
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_MANIFEST_STRICT = False

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ---------------------------------------------------
# PASSWORD VALIDATORS
# ---------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# ---------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'