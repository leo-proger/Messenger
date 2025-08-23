from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ConnectionHistory, UserProfile

User = get_user_model()


@receiver(post_save, sender=ConnectionHistory)
def send_online_status(sender, instance, created, **kwargs):
	if not created:
		user_id = instance.user.id
		if user_id:
			channel_layer = get_channel_layer()
			online_status = instance.online_status

			async_to_sync(channel_layer.group_send)(
				'online_users',
				{
					'type': 'send_online_status',
					'user_id': user_id,
					'online_status': online_status,
					}
				)


@receiver(post_save, sender=User)
def create_related_user_models(sender, instance, created, **kwargs):
	if created:
		ConnectionHistory.objects.create(user_id=instance.id)
		UserProfile.objects.create(user_id=instance.id)
