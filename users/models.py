import os

import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField


def validate_file_size(value):
	filesize = value.size
	max_size = 10 * 1024 * 1024  # 10 МБ
	if filesize > max_size:
		raise ValidationError("Размер файла превышает максимально допустимый размер (10 МБ).")


def get_user_image_path(instance, filename):
	return os.path.join('users', 'images', 'user_profile_images', str(instance.user.id),
	                    str(uuid.uuid4()) + '.' + filename.split('.')[-1])


def get_post_image_path(instance, filename):
	return os.path.join('users', 'images', 'user_post_images', str(instance.user.id), str(uuid.uuid4()))


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
	email = models.EmailField(
		max_length=255,
		unique=True,
		verbose_name=_('Электронная почта')
		)
	first_name = models.CharField(
		max_length=30,
		verbose_name=_('Имя')
		)
	last_name = models.CharField(
		max_length=30,
		verbose_name=_('Фамилия')
		)
	phone_number = PhoneNumberField(
		unique=True,
		null=True,
		blank=True,
		verbose_name=_('Номер телефона'),
		)
	is_active = models.BooleanField(
		default=True
		)
	is_staff = models.BooleanField(
		default=False
		)
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
		return f'{self.email} | {self.get_full_name()}'

	def get_full_name(self):
		full_name = f'{self.first_name} {self.last_name}'
		return full_name.strip()


class UserProfile(models.Model):
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='user_profile',
		)
	username = models.CharField(
		max_length=40,
		unique=True,
		blank=True,
		null=True,
		verbose_name=_('Имя пользователя'),
		)
	profile_image = ResizedImageField(
		size=[1024, 1024],
		crop=['middle', 'center'],
		upload_to=get_user_image_path,
		default='/users/images/user_profile_images/default_user_avatar.jpg',
		blank=True,
		verbose_name=_('Фотография'),
		validators=[FileExtensionValidator('JPEG JPG PNG SVG'.split()), validate_file_size],
		)
	age = models.PositiveSmallIntegerField(
		null=True,
		blank=True,
		verbose_name=_('Возраст'),
		)
	biography = models.TextField(
		max_length=500,
		blank=True,
		null=True,
		verbose_name=_('Биография'),
		)
	city = models.CharField(
		blank=True,
		null=True,
		verbose_name=_('Город'),
		max_length=168,
		)

	class Meta:
		verbose_name = _('Профиль пользователя')
		verbose_name_plural = _('Профили пользователей')

	def __str__(self):
		return self.user.email


class ConnectionHistory(models.Model):
	user = models.OneToOneField(
		CustomUser,
		on_delete=models.CASCADE,
		related_name='connection_history'
		)
	device_id = models.UUIDField(
		default=uuid.uuid4,
		editable=False,
		verbose_name=_('id устройства')
		)
	date_joined = models.DateField(
		auto_now_add=True,
		verbose_name=_('Дата регистрации')
		)
	last_online = models.DateTimeField(
		auto_now=True,
		null=True,
		blank=True,
		verbose_name=_('Время последнего входа')
		)
	online_status = models.BooleanField(
		default=False
		)

	class Meta:
		verbose_name = _('История подключений')
		verbose_name_plural = _('Истории подключений')

	def __str__(self):
		return self.user.email

	def update_online_status(self, online_status: bool):
		self.online_status = online_status
		self.last_online = timezone.now()
		self.save(update_fields=['online_status', 'last_online'])


class Post(models.Model):
	user = models.ForeignKey(
		CustomUser,
		on_delete=models.CASCADE,
		related_name='user_posts',
		verbose_name=_('Создатель поста'),
		)
	text = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		verbose_name=_('Текст поста'),
		)
	image = models.ImageField(
		upload_to=get_post_image_path,
		blank=True,
		null=True,
		verbose_name=_('Изображение поста'),
		)
	created = models.DateTimeField(
		auto_now_add=True,
		verbose_name=_('Время создания'),
		)

	class Meta:
		ordering = ['-created']
		verbose_name = _('Пост')
		verbose_name_plural = _('Посты')

	def __str__(self):
		return f'{self.id}'
