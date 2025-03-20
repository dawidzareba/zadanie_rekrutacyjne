"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import environ
from django.core.wsgi import get_wsgi_application

env = environ.Env()
env.read_env()

PROJECT_NAME = env("PROJECT_NAME")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{PROJECT_NAME}.settings")

application = get_wsgi_application()
