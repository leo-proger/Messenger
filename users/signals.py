import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ConnectionHistory

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=ConnectionHistory)
def send_online_status(sender, instance, created, **kwargs):
	if not created:
		channel_layer = get_channel_layer()
		user_id = instance.user.id
		online_status = instance.online_status

		async_to_sync(channel_layer.group_send)(
			f'online_users',
			{
				'type': 'send_online_status',
				'user_id': user_id,
				'online_status': online_status,
				}
			)
