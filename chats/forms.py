from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Value
from django.db.models.functions import Concat

from .models import Chat
from .models import Message

User = get_user_model()


class MessageForm(forms.ModelForm):
	message = forms.CharField(widget=forms.Textarea(
		attrs={
			'placeholder': 'Напишите сообщение...',
			'class': 'form-control message-input',
			}
		),
		required=True)

	class Meta:
		model = Message
		fields = ('message',)


class ChatCreateForm(forms.ModelForm):
	recipient = forms.ModelChoiceField(
		queryset=None,
		label='Собеседник',
		widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
		empty_label='Выберите собеседника',
		required=True
		)

	def __init__(self, user, *args, **kwargs):
		super(ChatCreateForm, self).__init__(*args, **kwargs)
		users = User.objects.exclude(id=user.id).annotate(
			full_name=Concat('first_name', Value(' '), 'last_name')
			)
		self.fields['recipient'].queryset = users
		self.fields['recipient'].label_from_instance = lambda obj: obj.full_name

	class Meta:
		model = Chat
		fields = ('recipient',)
		error_messages = {
			'recipient': {
				'required': 'Выберите собеседника',
				}
			}
