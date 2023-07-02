import uuid as uuid
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_resized import ResizedImageField

import os


def get_image_path(instance, filename):
	return os.path.join('users', 'images', 'user_profile_images', instance.user.email, filename)


class CustomUserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError(_('Электронная почта обязательна'))
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=255, unique=True, verbose_name=_('Электронная почта'))
	first_name = models.CharField(max_length=50, verbose_name=_('Имя'))
	last_name = models.CharField(max_length=50, verbose_name=_('Фамилия'))

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	user_permissions = models.ManyToManyField(
		'auth.Permission',
		blank=True,
		verbose_name=_('Права пользователя'),
		related_name='customuser_permissions',
		)

	objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	class Meta:
		verbose_name = _('Пользователь')
		verbose_name_plural = _('Пользователи')

	def __str__(self):
		return self.email

	def get_full_name(self):
		full_name = f'{self.first_name} {self.last_name}'
		return full_name.strip()


class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profiles')
	# При поиске будет не id пользователя, а username
	username = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name=_('Имя пользователя'))
	profile_image = ResizedImageField(
		size=[1024, 1024], crop=['middle', 'center'],
		upload_to=get_image_path,
		default='/users/images/user_profile_images/default_user_avatar.jpg', blank=True,
		verbose_name=_('Фотография'))
	biography = models.TextField(blank=True, null=True, verbose_name=_('Биография'))
	phone_number = PhoneNumberField(unique=True, null=True, blank=True, verbose_name=_('Номер телефона'))
	city = models.CharField(blank=True, null=True, verbose_name=_('Город'), max_length=168)

	class Meta:
		verbose_name = _('Профиль пользователя')
		verbose_name_plural = _('Профили пользователей')

	def __str__(self):
		return self.user.email


class ConnectionHistory(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	device_id = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name=_('id устройства'))
	date_joined = models.DateField(auto_now_add=True, verbose_name=_('Дата регистрации'))
	last_online = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Время последнего входа'))
	online_status = models.BooleanField(default=False)

	class Meta:
		verbose_name = _('История подключений')
		verbose_name_plural = _('Истории подключений')

	def __str__(self):
		return self.user.email

	def set_online(self):
		self.last_online = timezone.now()
		self.save(update_fields=['last_online'])

	def update_status(self, online_status):
		self.online_status = online_status
		self.save(update_fields=['online_status'])
