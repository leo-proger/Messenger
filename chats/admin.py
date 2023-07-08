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


admin.site.register(Chat, ChatAdmin)
