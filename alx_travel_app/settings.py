import os
from pathlib import Path
import environ
from celery.schedules import crontab
import dj_database_url

# ============================================================================
# Django Settings for ALX Travel App
# Consolidated configuration for local development and Render production
# ============================================================================

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment configuration
env = environ.Env(DEBUG=(bool, False))
env_file = BASE_DIR / '.env'
if env_file.exists():
    environ.Env.read_env(str(env_file))

# ============================================================================
# SECURITY
# ============================================================================
SECRET_KEY = env('SECRET_KEY', default='change-me-in-production')
DEBUG = env('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost', 'alx-travel-app.onrender.com'])

# ============================================================================
# INSTALLED APPS & MIDDLEWARE
# ============================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'listings',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alx_travel_app.urls'

# ============================================================================
# TEMPLATES
# ============================================================================
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

WSGI_APPLICATION = 'alx_travel_app.wsgi.application'

# ============================================================================
# DATABASE
# ============================================================================
DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}

DATABASES['default'] = dj_database_url.parse('postgresql://alx_travel_db_kai0_user:Uwe8vlrYDvGJk0EhCaEleFUOGuVAsWi3@dpg-d4d1ahripnbc739p6qk0-a.oregon-postgres.render.com/alx_travel_db_kai0')
# ============================================================================
# PASSWORD VALIDATION
# ============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================================
# INTERNATIONALIZATION
# ============================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ============================================================================
# STATIC & MEDIA FILES
# ============================================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# CORS & REST FRAMEWORK
# ============================================================================
CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=False)
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'http://localhost:3000',
    'https://alx-travel-app.onrender.com'
])

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}

# ============================================================================
# API DOCUMENTATION (drf-yasg)
# ============================================================================
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'api_key': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}
    },
}

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='no-reply@alxtravel.com')

# ============================================================================
# CELERY CONFIGURATION
# ============================================================================
# Broker and Result Backend: supports CELERY_BROKER_URL, UPSTASH_REDIS_URL, REDIS_URL
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default=env('UPSTASH_REDIS_URL', default=env('REDIS_URL', default='redis://localhost:6379/0')))
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default=env('UPSTASH_REDIS_URL', default=env('REDIS_URL', default='redis://localhost:6379/1')))
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes

# Celery Beat Schedule (periodic tasks)
CELERY_BEAT_SCHEDULE = {
    'cleanup-old-bookings': {
        'task': 'listings.tasks.cleanup_old_bookings',
        'schedule': crontab(hour=2, minute=0),  # 2 AM UTC daily
    },
    'send-booking-reminders': {
        'task': 'listings.tasks.send_booking_reminders',
        'schedule': crontab(minute=0),  # Every hour at :00
    },
}

# ============================================================================
# PAYMENT GATEWAY
# ============================================================================
CHAPA_SECRET_KEY = env('CHAPA_SECRET_KEY', default='')