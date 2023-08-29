from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserRegistrationForm, LoginForm, PostForm, EditProfileForm

User = get_user_model()


def about(request):
	return render(request, 'users/about.html')


def index(request):
	return render(request, 'users/index.html')


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
		login(self.request, self.object)

		return response


class UserLoginView(LoginView):
	template_name = 'users/login.html'
	form_class = LoginForm
	success_url = reverse_lazy('index')

	def form_valid(self, form, *args, **kwargs):
		response = super().form_valid(form)
		response.set_cookie('is_login', 'true')
		return super().form_valid(form)


def user_profile_view(request, user_id):
	user = get_object_or_404(User, id=user_id)

	if request.method == 'POST':
		post_form = PostForm(request.POST, request.FILES)

		if post_form.is_valid():
			post = post_form.save(commit=False)
			post.user = request.user
			post.save()
			return redirect('users:profile', user_id=user_id)
	else:
		post_form = PostForm()

	if request.user.id == user_id:
		user_online = 'online'
	else:
		user_online = is_online if (
			is_online := user.connection_history.online_status) else user.connection_history.last_online

	context = {
		'user_id': user_id,
		'user_full_name': user.get_full_name(),
		'user_profile_image': user.user_profile.profile_image,
		'user_biography': user.user_profile.biography.strip(),
		'user_posts': user.user_posts.all(),
		'user_online': user_online,

		'post_form': post_form,
		}

	return render(request, 'users/user_profile.html', context)


def edit_profile(request, user_id):
	user = get_object_or_404(User, id=user_id)
	user_profile = user.user_profile

	if request.method == 'POST':
		edit_profile_form = EditProfileForm(request.POST, request.FILES, instance=user_profile)

		if edit_profile_form.is_valid():
			edit_profile_form.save()
			return redirect('users:profile', user_id=user_id)
	else:
		edit_profile_form = EditProfileForm(instance=user_profile, initial={
			'first_name': user.first_name,
			'last_name': user.last_name,
			})

	context = {
		'user_id': user_id,
		'edit_profile_form': edit_profile_form,
		}

	return render(request, 'users/edit_profile.html', context)
