"""
Django settings for stunotes project.
Optimized for deployment on Vercel using Supabase PostgreSQL.
"""

import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
from decouple import config
import cloudinary

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
# FIX: Convert the comma-separated string to a list for proper host checking
ALLOWED_HOSTS = [host.strip() for host in raw_allowed.split(',')] if raw_allowed else []
if DEBUG:
    ALLOWED_HOSTS.append('localhost')
    ALLOWED_HOSTS.append('127.0.0.1')
    ALLOWED_HOSTS.append('[::1]') # IPv6 local host

# CSRF trusted origins for prod
raw_csrf = config('CSRF_TRUSTED_ORIGINS', default='')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in raw_csrf.split(',')] if raw_csrf else []


# ---------------------------------------------------
# APPLICATIONS
# ---------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',  # Must be BEFORE staticfiles
    'cloudinary',
    'django.contrib.staticfiles',  # Only once!
    'notes',
    'widget_tweaks',
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
# SESSION MANAGEMENT (Auto Logout, Stay Signed In)
# ---------------------------------------------------

# Controls "Stay Signed In" and maximum session lifetime.
# SETTINGS:
# - True: Logs out when the browser is closed (Good for public/shared computers).
# - False: Keeps the session active until SESSION_COOKIE_AGE expires (Default, "Stay Signed In").
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Maximum age of the session cookie, in seconds. 
# Used when SESSION_EXPIRE_AT_BROWSER_CLOSE is False.
# Value below is 7 days (7 * 24 * 60 * 60 = 604800)
SESSION_COOKIE_AGE = 604800 

# CRITICAL SECURITY SETTINGS (MUST BE TRUE IN PRODUCTION)
# Ensure cookies are only sent over HTTPS/SSL.
SESSION_COOKIE_SECURE = not DEBUG 
# Prevent client-side JavaScript access to the cookie (XSS defense).
SESSION_COOKIE_HTTPONLY = True 
# Helps protect against CSRF and cross-site requests.
SESSION_COOKIE_SAMESITE = 'Lax' 

# ---------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------
AUTH_USER_MODEL = 'notes.User'
LOGIN_URL = 'notes:login'


# ---------------------------------------------------
# CLOUDINARY CONFIGURATION (Media Files)
# ---------------------------------------------------
cloudinary.config(
    cloud_name = config('CLOUDINARY_CLOUD_NAME', default=''),
    api_key = config('CLOUDINARY_API_KEY', default=''),
    api_secret = config('CLOUDINARY_API_SECRET', default='')
)

# Use Cloudinary for all media file storage
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# ---------------------------------------------------
# STATIC FILES
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

# Media URL (served by Cloudinary)
MEDIA_URL = '/media/'

# Secure cookies for production
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = False  # CSRF must be readable by browser, keep default
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=not DEBUG, cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=0 if DEBUG else 31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG


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