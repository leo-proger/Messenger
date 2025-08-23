from django.urls import path

from users.views import *

app_name = 'users'

urlpatterns = [
	path('registration/', UserRegistrationView.as_view(), name='register'),
	path('login/', UserLoginView.as_view(), name='login'),
	path('profile/<int:user_id>/', user_profile_view, name='profile'),
	path('edit-profile/<int:user_id>/', edit_profile, name='edit-profile'),
	# path('upload-post/<int:user_id>/', upload_post, name='upload-post'),
	]
