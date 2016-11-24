from cashflow.settings.base import *

SECRET_KEY = '2lx(34sh*3o64*d#%p@+(-0fp*xz=z5qbl(!@*&(i-x)&(&77g'

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_ROOT = 'staticfiles'
