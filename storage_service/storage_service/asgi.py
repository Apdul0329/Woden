import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

from columns.routings import websocket_urlpatterns as columns_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storage_service.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': URLRouter(
        columns_urlpatterns
    )
})


