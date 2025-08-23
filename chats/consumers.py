import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from notifications.signals import notify

from .models import Chat, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
	def __init__(self, *args, **kwargs):
		super().__init__(args, kwargs)
		self.chat_uuid = None
		self.room_group_name = None

	async def connect(self):
		self.chat_uuid = self.scope['url_route']['kwargs']['chat_uuid']
		self.room_group_name = f'Chat_{self.chat_uuid}'

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

	# Когда из js вызываешь функцию Socket.send() и то, что в скобках придет в виде text_data
	async def receive(self, text_data=None, **kwargs):
		text_data_json = json.loads(text_data)
		chat_uuid = text_data_json['chat_uuid']
		message = text_data_json['message']

		await self.save_message(
			chat_uuid,
			message,
			)

	# Эта функция отправляет сообщение и в js принять ее функцией Socket.onmessage
	async def chat_message(self, event):
		message = event['message']
		sender_id = event['sender_id']

		await self.send(text_data=json.dumps({
			'sender_id': sender_id,
			'message': message,
			}))

	@database_sync_to_async
	def save_message(self, chat_uuid, message):
		if message.split():
			sender_id = self.scope['user'].id
			chat = Chat.objects.get(uuid=chat_uuid)
			recipient = chat.members.exclude(id=sender_id).first()

			Message.objects.create(chat=chat, sender_id=sender_id, recipient=recipient, message=message.strip())

			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name,
				# Этот словарь идет как параметр event в метод chat_message
				{
					'type': 'chat_message',
					'sender_id': sender_id,
					'message': message,
					}
				)


class NotificationConsumer(AsyncWebsocketConsumer):
	def __init__(self, *args, **kwargs):
		super().__init__(args, kwargs)
		self.room_group_name = None

	async def connect(self):
		self.room_group_name = f"message_notifications_{self.scope['url_route']['kwargs']['user_id']}"
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

	async def receive(self, text_data=None, **kwargs):
		pass

	async def send_notification(self, event):
		chat_uuid = event['chat_uuid']

		actor = await database_sync_to_async(User.objects.get)(email=event['actor'])
		recipient = await database_sync_to_async(User.objects.get)(email=event['recipient'])
		chat = await database_sync_to_async(Chat.objects.get)(uuid=chat_uuid)
		verb = event['verb']

		last_chat_message = event['last_chat_message']

		await sync_to_async(notify.send)(actor, recipient=recipient, target=chat, verb=verb)
		await self.send(text_data=json.dumps({
			'type': 'new_message',
			'chat_uuid': chat_uuid,
			'last_chat_message': last_chat_message,
			}))
