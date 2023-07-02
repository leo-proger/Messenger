import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from users.models import ConnectionHistory

User = get_user_model()


class OnlineStatusConsumer(AsyncWebsocketConsumer):
	def __init__(self, *args, **kwargs):
		super().__init__(args, kwargs)
		self.user = None
		self.room_group_name = None

	async def connect(self):
		self.user = self.scope['user']
		self.room_group_name = f'online_users'

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
			)

		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
			)

	async def receive(self, text_data=None, bytes_data=None):
		data = json.loads(text_data)
		online_status = data['online_status']

		await self.update_user_online_status(self.user, online_status)

	async def send_online_status(self, event):
		user = event['user']
		online_status = event['online_status']

		await self.send(text_data=json.dumps({
			'user': user,
			'online_status': online_status,
			}))

	@database_sync_to_async
	def update_user_online_status(self, user, online_status):
		user_connection_history = ConnectionHistory.objects.get_or_create(user=user)[0]
		user_connection_history.online_status = online_status
		user_connection_history.save()

		async_to_sync(self.channel_layer.group_send)(
			'online_users',
			{
				'type': 'send_online_status',
				'user': str(user),
				'online_status': online_status
				}
			)
