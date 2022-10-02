import os
from .default import *

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']
