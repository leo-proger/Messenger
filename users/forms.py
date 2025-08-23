from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from users.models import UserProfile, Post

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField()
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)
	first_name = forms.RegexField(regex=r'^[a-zA-Zа-яА-Я]', max_length=30)
	last_name = forms.RegexField(regex=r'^[a-zA-Zа-яА-Я]', max_length=30)

	class Meta:
		model = User
		fields = ('email', 'password1', 'password2', 'first_name', 'last_name')

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise ValidationError(_('Пароли не совпадают'))
		return password2


class LoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.EmailInput({'required': '', 'name': '', 'type': 'text'}))
	password = forms.CharField(
		widget=forms.PasswordInput({'required': '', 'name': '', 'type': 'password', 'autocomplete': 'new-password'}))


class UserProfileForm(forms.ModelForm):
	username = forms.CharField(max_length=50, required=False)
	profile_image = forms.ImageField(required=False, label=_('Фотография'))
	biography = forms.CharField(widget=forms.Textarea, required=False, label=_('Биография'))
	phone_number = PhoneNumberField(required=True, label=_('Номер телефона'))
	city = forms.CharField(required=False, label=_('Город'))
	country = forms.CharField(required=False, label=_('Страна'))

	class Meta:
		model = UserProfile
		fields = ('profile_image', 'biography', 'phone_number', 'city', 'country')


class MessageForm(forms.Form):
	text = forms.CharField(label=_('Текст сообщение'), widget=forms.Textarea())


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['text', 'image']
		labels = {
			'text': '',
			'image': '',
			}
		widgets = {
			'text': forms.Textarea(attrs={
				'id': 'create-post__input-text',
				'placeholder': 'Текст поста',
				'rows': '1',
				}),
			'image': forms.FileInput(attrs={
				'id': 'create-post__select-image',
				'style': 'display: none',
				}),
			}

	def clean(self):
		text = self.cleaned_data.get('text')
		image = self.cleaned_data.get('image')

		if not text and not image:
			raise ValidationError(_('Пост не может быть пустым'))

		return self.cleaned_data


class EditProfileForm(forms.ModelForm):
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)

	class Meta:
		model = UserProfile
		fields = ('first_name', 'last_name', 'profile_image', 'biography', 'username', 'age', 'city')
