from django.contrib.auth import get_user_model

User = get_user_model()


def current_user_image(request):
	if request.user.is_authenticated:
		image = request.user.user_profile.profile_image
		return {'current_user_image': image}
	return ''


def current_user_id(request):
	if request.user.is_authenticated:
		return {'current_user_id': request.user.id}
	return ''


def current_user_full_name(request):
	if request.user.is_authenticated:
		return {'current_user_full_name': request.user.get_full_name()}
	return ''
