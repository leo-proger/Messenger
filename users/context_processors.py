from django.contrib.auth import get_user_model

User = get_user_model()


def current_user_image(request):
	if request.user.is_authenticated:
		icon = request.user.user_profiles.profile_image
		return {'user_photo': icon}
	return ''


def current_user_email(request):
	if request.user.is_authenticated:
		return {'current_user_email': request.user.email}
	return ''


def current_user_id(request):
	if request.user.is_authenticated:
		return {'current_user_id': request.user.id}
	return ''


def current_user_full_name(request):
	if request.user.is_authenticated:
		return {'current_user_full_name': request.user.get_full_name()}
	return ''
