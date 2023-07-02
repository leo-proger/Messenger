from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html

from chats.admin import ChatInline
from users.models import UserProfile, ConnectionHistory

User = get_user_model()


class CustomUserAdmin(admin.ModelAdmin):
	def profile_link(self, obj):
		url = "/admin/users/userprofile/{}/".format(obj.user_profiles.id)
		return format_html('<a href="{}">View Profile</a>', url)

	def chat_list(self, obj):
		chats = obj.chats.all()
		return ', '.join([str(chat) for chat in chats])

	chat_list.short_description = 'Chats'

	profile_link.short_description = 'Profile'
	profile_link.admin_order_field = 'user_profile__id'

	list_display = ('email', 'first_name', 'last_name', 'profile_link', 'chat_list')
	readonly_fields = ('profile_link',)

	ordering = ('email',)
	inlines = [ChatInline]


class UserProfileAdmin(admin.ModelAdmin):
	ordering = ('user__email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ConnectionHistory)
