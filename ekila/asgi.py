"""
ASGI config for ekila project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information, refer to:
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
https://channels.readthedocs.io/en/stable/
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ekila.settings")

application = get_asgi_application()
