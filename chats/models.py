import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Chat(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	group_name = models.CharField(max_length=100, unique=True, editable=False)
	members = models.ManyToManyField(User, related_name='chats')  # Получить все сообщения, связанные с пользователем
	created_by = models.ForeignKey(User, on_delete=models.CASCADE,
	                               related_name='chats_created')  # Получить все чаты, созданные пользователем
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Чат'
		verbose_name_plural = 'Чаты'
		ordering = ('-created_at',)

	def __str__(self):
		return f'Chat {self.id}'

	def get_group_name(self):
		return f'Chat_{str(self.uuid)}'

	def save(self, *args, **kwargs):
		if not self.group_name:
			self.group_name = f'Chat_{str(self.uuid)}'
		super().save(*args, **kwargs)


class Message(models.Model):
	chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='messages')
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
	recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='received_messages')
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Сообщение'
		verbose_name_plural = 'Сообщения'
		ordering = ('created_at',)

	def __str__(self):
		return f'Message {self.id}'
