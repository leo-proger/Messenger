from django import template
from django.utils.text import Truncator

from users.models import UserProfile, ConnectionHistory

register = template.Library()


@register.filter
def next(some_list, current_index):
	try:
		return some_list[int(current_index) + 1]
	except:
		return ''


@register.filter
def previous(some_list, current_index):
	try:
		return some_list[int(current_index) - 1]
	except:
		return some_list[int(current_index)]
