from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView

from .forms import UserRegistrationForm, LoginForm
from .models import UserProfile, ConnectionHistory


def about(request):
	return render(request, 'users/about.html')


def index(request):
	return render(request, 'users/index.html')


# def check_online(request, user=None):
# 	user = user or request.user
# 	now = timezone.now()
# 	online_threshold = now - timezone.timedelta(seconds=30)
# 	is_online = user.last_online is not None and user.last_online > online_threshold
# 	user.set_online()
# 	return JsonResponse({'is_online': is_online})


# def user_register(request):
# 	if request.method.lower() == 'post':
# 		form = RegisterForm(request.POST)
# 		if form.is_valid():
# 			user = form.save()
# 			UserProfile.objects.create(user=user)
# 			login(request, user)
# 			messages.success(request, 'Регистрация прошла успешно!')
# 			return redirect('index')
# 	else:
# 		form = RegisterForm()
# 	return render(request, 'users/register.html', {'form': form})

class UserRegistrationView(CreateView):
	template_name = 'users/register.html'
	form_class = UserRegistrationForm
	success_url = reverse_lazy('index')

	def form_valid(self, form):
		response = super().form_valid(form)
		UserProfile.objects.create(user=self.object)
		ConnectionHistory.objects.create(user=self.object)

		login(self.request, self.object)
		return response


class UserLoginView(LoginView):
	template_name = 'users/login.html'
	form_class = LoginForm
	success_url = reverse_lazy('index')

	def form_valid(self, form, *args, **kwargs):
		response = super().form_valid(form)
		response.set_cookie('is_login', 'true')
		messages.success(self.request, 'Авторизация прошла успешно!')
		return super().form_valid(form)


# class UserProfileView(TemplateView):
# 	pass

def user_profile_view(request, user_id):
	return render(request, 'users/user_profile.html', context={'user_id': user_id})
