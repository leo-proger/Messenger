from django.urls import path

from chats.views import *

app_name = 'chats'

urlpatterns = [
	path('', chats_view, name='chat_list'),
	path('<uuid:chat_uuid>/', chats_view, name='chat_detail'),
	path('create-chat/', ChatCreateView.as_view(), name='create_chat'),
	path('<uuid:chat_uuid>/delete_chat/', ChatDeleteView.as_view(), name='delete_chat'),
	]
