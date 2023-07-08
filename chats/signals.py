from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
	if created:
		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
			f'message_notifications_{instance.receiver.id}',
			{
				'type': 'send_notification',
				'recipient': instance.receiver.email,
				'chat_uuid': str(instance.chat.uuid),
				'last_chat_message': instance.message,
				'verb': 'received a new message',
				}
			)
