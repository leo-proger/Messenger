from django.contrib.auth import get_user_model

User = get_user_model()


def user_photo(request):
	if request.user.is_authenticated:
		icon = request.user.user_profiles.profile_image
		return {'user_photo': icon}
	return ''


def current_user(request):
	if request.user.is_authenticated:
		return {'current_user': request.user.email}
	return ''
