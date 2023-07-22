from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone

User = get_user_model()


class AuthMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if not request.user.is_authenticated and not request.path == reverse_lazy(
				'users:login') and not request.path == reverse_lazy('users:register'):
			return redirect(reverse_lazy('users:login'))
		response = self.get_response(request)
		return response


class SuperuserCheckMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if request.path.startswith('/admin/') and not request.user.is_superuser:
			return HttpResponseRedirect(reverse('index'))
		response = self.get_response(request)
		return response
