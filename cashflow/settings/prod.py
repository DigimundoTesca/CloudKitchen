from cashflow.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['dabbanet.dabbawala.com.mx', 'dabbawala.com.mx']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DABBANET_DB_NAME'),
        'USER': os.getenv('DABBANET_DB_USER'),
        'PASSWORD': os.getenv('DABBANET_DB_PASSWORD'),
        'HOST': os.getenv('DABBANET_DB_HOST'),
        'PORT': os.getenv('DABBANET_DB_PORT'),
    }
}

STATIC_ROOT = 'staticfiles'

MEDIA_URL = '/'
