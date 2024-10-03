from pathlib import Path
from datetime import datetime, timedelta
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'your-secret-key'
DEBUG = False
FROM_EMAIL = 'motheakash11@gmail.com'

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'silk',
]

CUSTOME_APPS = [
    'apps.core',
    'apps.authentications',
    'apps.member_management',
    'apps.product_management',
]

INSTALLED_APPS.extend(CUSTOME_APPS)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database configuration (example for SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shopcart',
        'USER': os.environ.get('BM_DB_USER'),
        'PASSWORD': os.environ.get('BM_DB_PASSWORD'),
        'HOST': 'localhost',  # Or replace with your database host
        'PORT': '5432', 
    }
}

# print(os.environ.get('BM_DB_USER'))
# print(os.environ.get('BM_DB_PASSWORD'))

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': 60,  # in minute
    'REFRESH_TOKEN_LIFETIME': 1,     # in day
    'JWT_ALGORITHM': 'HS256',
    'SECRETE_KEY': 'tokensecretkey',
}

ROLE_PERMISSIONS = {
    'Viewer': ['GET'],
    'Admin': ['GET', 'PATCH', 'POST', 'PUT', 'DELETE'],
    'Editor': ['PATCH', 'PUT']
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'django_sql.log'),
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#         'django': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }