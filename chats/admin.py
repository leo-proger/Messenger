from django.contrib import admin

from .models import Chat, Message


class ChatInline(admin.TabularInline):
	model = Chat
	extra = 0


class MessageInline(admin.TabularInline):
	model = Message
	extra = 0


class ChatAdmin(admin.ModelAdmin):
	inlines = [MessageInline]


class MessageAdmin(admin.ModelAdmin):
	list_display = ('chat', 'message_display')

	def message_display(self, obj):
		return f'MessageOfChat_{obj.id}'


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
