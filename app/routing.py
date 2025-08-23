from django.urls import re_path, path

from chats.consumers import ChatConsumer, NotificationConsumer
from users.consumers import OnlineStatusConsumer

websocket_urlpatterns = [
	re_path(r'^ws/chats/(?P<chat_uuid>[^/]+)/$', ChatConsumer.as_asgi()),
	re_path(r'^ws/online/$', OnlineStatusConsumer.as_asgi()),
	re_path(r'^ws/message-notifications/(?P<user_id>[^/]+)/$', NotificationConsumer.as_asgi()),
	]
