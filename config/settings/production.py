from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'prod_db_name',
        'USER': 'prod_user',
        'PASSWORD': 'prod_password',
        'HOST': 'prod_db_host',
        'PORT': '5432',
    }
}