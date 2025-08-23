import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from app.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
	"http": asgi_application,
	"websocket": AuthMiddlewareStack(
		URLRouter(
			websocket_urlpatterns
			)
		),
	})
