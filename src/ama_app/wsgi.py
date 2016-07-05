"""
WSGI config for ama_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings
import mongoengine as mongo
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ama_app.deb")

mongo.connect(settings.MONGO_DATABASE, 
        host=settings.MONGO_HOST, 
        username=settings.MONGO_USER, 
        password=settings.MONGO_PASSWORD
        )

logging.basicConfig(filename=os.path.join(settings.LOG_PATH, settings.LOG_NAME),
        format='[%(levelname)s]%(asctime)s %(filename)s[method:%(funcName)s, line:%(lineno)d] %(message)s',
        level=logging.DEBUG,
        filemode='a',
        )

application = get_wsgi_application()
