from django.urls import re_path, path

from chats.consumers import ChatConsumer
from users.consumers import OnlineStatusConsumer

websocket_urlpatterns = [
	re_path(r'^ws/chats/(?P<chat_uuid>[^/]+)/$', ChatConsumer.as_asgi()),
	re_path(r'^ws/online/$', OnlineStatusConsumer.as_asgi())
	]
