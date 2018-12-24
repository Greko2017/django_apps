"""
WSGI config for blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from whitenoise import WhiteNoise

from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

application = get_wsgi_application()

application = WhiteNoise(application, root=STATIC_ROOT)
application.add_files(os.path.join(BASE_DIR), "static")