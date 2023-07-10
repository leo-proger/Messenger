from django.contrib import admin

from .models import Chat, Message


class ChatInline(admin.TabularInline):
	model = Chat
	extra = 0


class MessageInline(admin.TabularInline):
	model = Message
	extra = 0
	ordering = ('-created_at',)


class ChatAdmin(admin.ModelAdmin):
	inlines = [MessageInline]
	ordering = ('-created_at',)
	list_display = ('display_chat', 'get_members_full_names', 'get_members_emails')

	def display_chat(self, obj):
		return str(obj)

	display_chat.short_description = 'Chat'

	def get_members_full_names(self, obj):
		return " | ".join([str(member.get_full_name()) for member in obj.members.all()])

	get_members_full_names.short_description = 'Members Full Names'

	def get_members_emails(self, obj):
		return " | ".join([str(member.email) for member in obj.members.all()])

	get_members_emails.short_description = 'Members Emails'


admin.site.register(Chat, ChatAdmin)
