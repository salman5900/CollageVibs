"""
ASGI config for mark1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mark1.settings')

django_asgi_app = get_asgi_application()

from globalchat.routing import websocket_urlpatterns as globalchat_patterns
from clubs.routing import websocket_urlpatterns as clubs_patterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                globalchat_patterns + clubs_patterns 
            )
        )
    ),
})
