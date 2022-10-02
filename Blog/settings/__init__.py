import os

environment = os.environ.get("DJANGO_ENVIRONMENT")

if environment == 'production':
    from .production import *
else:
    from .default import *
