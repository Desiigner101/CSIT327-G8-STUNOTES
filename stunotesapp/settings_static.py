"""
Minimal Django settings used only during the build step to run collectstatic.
This avoids importing full INSTALLED_APPS and thus prevents database backend imports
on build machines that may not have sqlite3 available.
"""
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Minimal required settings
SECRET_KEY = config('SECRET_KEY', default='django-insecure-static-placeholder')
DEBUG = True

# Static
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_cdn'
STATICFILES_DIRS = [BASE_DIR / 'notes' / 'static']

# Only the staticfiles app is needed to collect static assets
INSTALLED_APPS = [
    'django.contrib.staticfiles',
]

# Minimal middleware (not strictly required for collectstatic)
MIDDLEWARE = []

# Avoid database imports
DATABASES = {}
