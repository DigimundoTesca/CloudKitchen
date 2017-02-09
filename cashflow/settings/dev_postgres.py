from cashflow.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

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

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}
