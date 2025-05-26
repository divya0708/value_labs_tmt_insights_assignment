from .base import *

# Disable debug mode for production
DEBUG = False

# Replace '*' with actual production domain(s) or IPs for security
ALLOWED_HOSTS = ['*']

# PostgreSQL production database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'prod_db_name',     # Replace with production DB name
        'USER': 'prod_user',        # Replace with production DB user
        'PASSWORD': 'prod_password',# Replace with production DB password
        'HOST': 'prod_db_host',     # Replace with production DB host
        'PORT': '5432',             # Default PostgreSQL port
    }
}
