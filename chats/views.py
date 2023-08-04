from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from notifications.models import Notification

from users.models import UserProfile, ConnectionHistory
# from users.views import check_online
from .forms import MessageForm, ChatCreateForm
from .models import Chat, Message

User = get_user_model()


class ChatCreateView(CreateView):
	model = Chat
	template_name = 'chats/create_chat.html'
	form_class = ChatCreateForm
	success_url = reverse_lazy('chats:chat_list')

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['user'] = self.request.user.email
		return kwargs

	def form_valid(self, form):
		recipient = form.cleaned_data['recipient']
		# existing_chat = Chat.objects.filter(members=recipient).distinct().first()

		# if existing_chat:
		# 	return redirect('chats:chat_detail', chat_uuid=existing_chat.uuid)
		# else:
		chat = Chat.objects.create(created_by=self.request.user.email)
		chat.members.add(self.request.user.email, recipient)
		return redirect('chats:chat_detail', chat_uuid=chat.uuid)


class ChatDeleteView(DeleteView):
	model = Chat
	success_url = reverse_lazy('chats:chat_list')

	def delete(self, request, *args, **kwargs):
		chat = self.get_object()
		chat.delete()
		return redirect(self.get_success_url())


def is_ajax(request):
	return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or 'XMLHttpRequest' in request.headers.get(
		'Accept', '')


def chats_view(request, chat_uuid=None):
	chat_list = request.user.chats.all()
	chats = []

	for chat in chat_list:
		recipient = chat.members.exclude(pk=request.user.pk).first()
		recipient_image = UserProfile.objects.get(user=recipient).profile_image
		recipient_online = ConnectionHistory.objects.get(user=recipient).online_status
		last_chat_message = msg if (msg := Message.objects.filter(chat=chat).last()) else ''
		last_chat_message_time = last_chat_message.created_at if last_chat_message else ''
		unread_count = Notification.objects.filter(recipient=request.user.id, target_object_id=chat.id,
		                                           unread=True, verb='received a new message').count()
		chats.append((
			chat,
			recipient,
			recipient_image,
			recipient_online,
			last_chat_message.message,
			last_chat_message_time,
			unread_count,
			))

	chats = sorted(chats, key=lambda x: x[5], reverse=True)

	if chat_uuid:
		chat = request.user.chats.filter(uuid=chat_uuid).first()
		if not chat:
			return redirect('chats:chat_list')

		messages = Message.objects.filter(chat=chat)
		recipient = chat.members.exclude(pk=request.user.pk).first()
		recipient_image = recipient.user_profile.profile_image
		recipient_online = ConnectionHistory.objects.get(user=recipient).online_status
		form = None

		Notification.objects.filter(recipient=request.user, target_object_id=chat.id).delete()

		if request.method == 'POST':
			form = MessageForm(request.POST)
			if form.is_valid():
				return redirect('chats:chat_detail', chat_uuid=chat_uuid)

		if form is None:
			form = MessageForm()

		context = {
			'messages': messages,
			'recipient': recipient,
			'recipient_image': recipient_image,
			'recipient_online': recipient_online,
			'current_user': request.user.email,

			'chats': chats,
			'chat_uuid': chat_uuid,
			'chat_content': True,

			'form': form,
			}
	else:
		context = {
			'chats': chats,
			'chat_content': False,
			}
	return render(request, 'chats/chats.html', context)
