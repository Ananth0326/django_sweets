import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ---
# PRODUCTION/DEPLOYMENT SETTINGS
# ---
# We read these from Vercel's Environment Variables
#
# !! IMPORTANT !!
# Do NOT hardcode your secret key here.
SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG is set to False in production by the 'DJANGO_DEBUG' environment variable
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# Get allowed hosts from environment variable, split by comma
allowed_hosts_string = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = allowed_hosts_string.split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Add whitenoise for serving static files
    'whitenoise.storage.CompressedManifestStaticFilesStorage',
    'django.contrib.staticfiles',
    'testapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Add whitenoise middleware RIGHT AFTER security middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sweetspot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Tell Django to look for templates in the 'testapp/templates' directory
        'DIRS': [BASE_DIR / 'testapp' / 'templates'],
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

WSGI_APPLICATION = 'sweetspot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Vercel has an ephemeral file system, so we use sqlite here.
# The 'migrate' command in our build step will create this file on every deploy.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I1N = True
USE_TZ = True


# ---
# STATIC & MEDIA FILES (FOR PRODUCTION)
# ---

# This is where 'collectstatic' will gather all static files
STATIC_ROOT = BASE_DIR / 'staticfiles'

# This is the URL static files will be served from (e.g., /static/style.css)
STATIC_URL = '/static/'

# This tells Django where to find your app's static files (style.css, images)
STATICFILES_DIRS = [
    BASE_DIR / "testapp" / "static",
]

# This tells whitenoise to handle static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# This is for user-uploaded images (your sweet_images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

