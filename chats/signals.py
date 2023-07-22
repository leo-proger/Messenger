from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from notifications.signals import notify

from .models import Message
from users.models import ConnectionHistory


@receiver(post_save, sender=Message)
def new_message_notification(sender, instance, created, **kwargs):
	if created:
		recipient_online = ConnectionHistory.objects.get(user_id=instance.recipient.id).online_status

		verb = 'received a new message'

		if recipient_online:
			actor = instance.sender.email
			recipient = instance.recipient.email

			channel_layer = get_channel_layer()
			async_to_sync(channel_layer.group_send)(
				f'message_notifications_{instance.recipient.id}',
				{
					'type': 'send_notification',
					'actor': actor,
					'recipient': recipient,
					'chat_uuid': str(instance.chat.uuid),
					'verb': verb,
					'last_chat_message': instance.message,
					}
				)
		else:
			actor = instance.sender
			recipient = instance.recipient
			target = instance.chat

			notify.send(actor, recipient=recipient, target=target, verb=verb)
