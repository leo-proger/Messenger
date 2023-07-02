import json

from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

# from users.views import check_online
from .forms import MessageForm, ChatCreateForm
from .models import Chat, Message
from users.models import UserProfile, ConnectionHistory

User = get_user_model()


# @never_cache
# def chat_detail(request, chat_uuid):
# 	chat = get_object_or_404(Chat, uuid=chat_uuid)
# 	messages = Message.objects.filter(chat=chat)
# 	# companion = chat.members.exclude(id=request.user.id).first()
# 	current_user = request.user
# 	# companion_connection_history = ConnectionHistory.objects.get_or_create(user=companion)[0]
# 	# companion_online = companion_connection_history.online_status
#
# 	user = request.user
# 	chats = Chat.objects.filter(members=user)
# 	chats_and_companions = []
# 	for chat in chats:
# 		companions = chat.members.exclude(pk=user.pk)
# 		chats_and_companions.append((chat, companions))
#
# 	if request.method == 'POST':
# 		form = MessageForm(request.POST)
# 		if form.is_valid():
# 			return redirect('chats:chat_detail', chat_uuid=chat_uuid)
# 	else:
# 		form = MessageForm()
#
# 	context = {
# 		'form': form,
# 		'chat_uuid': chat_uuid,
# 		'messages': messages,
# 		# 'companion': companion.get_full_name(),
# 		# 'companion_id': companion.id,
# 		# 'companion_online': companion_online,
# 		'current_user': current_user.email,
# 		'current_user_full_name': current_user.get_full_name(),
# 		'chats': chats_and_companions
# 		}
# 	return render(request, 'chats/chat_detail.html', context)

class ChatCreateView(CreateView):
	model = Chat
	template_name = 'chats/create_chat.html'
	form_class = ChatCreateForm
	success_url = reverse_lazy('chats:chat_list')

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		companion = form.cleaned_data['companion']
		# existing_chat = Chat.objects.filter(members=companion).distinct().first()

		# if existing_chat:
		# 	return redirect('chats:chat_detail', chat_uuid=existing_chat.uuid)
		# else:
		chat = Chat.objects.create(created_by=self.request.user)
		chat.members.add(self.request.user, companion)
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
	# ----
	chat_list = request.user.chats.all()
	chats = []

	for chat in chat_list:
		companion = chat.members.exclude(pk=request.user.pk).first()
		companion_image = UserProfile.objects.get(user=companion).profile_image
		companion_online = ConnectionHistory.objects.get_or_create(user_id=companion.id)[0].online_status
		last_chat_message = Message.objects.filter(chat=chat).last()
		last_chat_message_time = last_chat_message.created_at if last_chat_message else ''
		chats.append((
			chat,
			companion.get_full_name(),
			companion_image,
			companion_online,
			last_chat_message.message if last_chat_message else '',
			last_chat_message_time,
			))
	# ----

	if chat_uuid:
		chat = Chat.objects.get(uuid=chat_uuid)
		messages = Message.objects.filter(chat=chat)
		companion = chat.members.exclude(id=request.user.id).first()
		companion_image = companion.user_profiles.profile_image
		companion_online = ConnectionHistory.objects.get_or_create(user_id=companion.id)[0].online_status

		context = {
			'messages': messages,
			'companion': companion.get_full_name(),
			'companion_image': companion_image,
			'companion_online': companion_online,
			'current_user': request.user.email,

			'chats': chats,
			'chat_uuid': chat_uuid,
			'chat_content': True,
			}
		return render(request, 'chats/chats.html', context)
	else:
		context = {
			'chats': chats,
			'chat_content': False,
			}
		return render(request, 'chats/chats.html', context)
