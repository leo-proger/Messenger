from django import template
from django.template.defaultfilters import date as _date
from django.utils import timezone

register = template.Library()


def plural_form(n, forms):
	if n % 10 == 1 and n % 100 != 11:
		form = 0
	elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
		form = 1
	else:
		form = 2
	return str(n) + ' ' + forms[form]


@register.filter
def last_online_format(last_online_time):
	try:
		# Получаем текущее время
		now = timezone.now()

		# Вычисляем разницу между текущим временем и временем последнего онлайна
		diff = now - last_online_time

		# Прошедшее время в секундах
		elapsed_seconds = diff.total_seconds()

		# Прошедшее время в днях
		days_difference = diff.days

		# Форматы времени
		minute_form = ['минуту', 'минуты', 'минут']
		week_form = ['неделю', 'недели', 'недель']
		month_form = ['месяц', 'месяца', 'месяцев']

		# Пользователь был в сети менее минуты назад
		if elapsed_seconds < 60:
			return 'был(a) в сети недавно'

		# Пользователь был в сети менее часа назад
		elif elapsed_seconds < 60 * 60:
			minutes = int(elapsed_seconds // 60)
			return "был(a) в сети {} назад".format(plural_form(minutes, minute_form))

		# Пользователь был в сети вчера
		elif last_online_time.date() == now.date() - timezone.timedelta(days=1):
			time_str = "{}:{}".format(last_online_time.hour,
			                          str(last_online_time.minute).zfill(2))  # Использование zfill(2)
			return 'был(a) в сети вчера в {}'.format(time_str)

		# Пользователь был в сети в течение последней недели
		elif last_online_time.date() > now.date() - timezone.timedelta(days=7):
			date_str = _date(last_online_time, "l")
			time_str = "{}:{}".format(last_online_time.hour,
			                          str(last_online_time.minute).zfill(2))  # Использование zfill(2)
			return 'был(a) в сети в {} в {}'.format(date_str, time_str)

		# Пользователь был в сети в течение последнего месяца
		elif last_online_time.date() > now.date() - timezone.timedelta(days=30):
			weeks = days_difference // 7
			return "был(a) в сети {} назад".format(plural_form(weeks, week_form))

		# Пользователь был в сети в течение последнего года
		elif last_online_time.date() > now.date() - timezone.timedelta(days=365):
			months = days_difference // 30
			return "был(a) в сети {} назад".format(plural_form(months, month_form))

		# Пользователь был в сети более года назад
		else:
			return 'был(a) в сети более года назад'
	except TypeError:
		# Если last_online_time не является датой/временем, возвращаем 'online'
		return 'online'


@register.filter
def post_date_format(value):
	months = {
		1: 'янв',
		2: 'фев',
		3: 'мар',
		4: 'апр',
		5: 'май',
		6: 'июн',
		7: 'июл',
		8: 'авг',
		9: 'сен',
		10: 'окт',
		11: 'ноя',
		12: 'дек'
		}
	now = timezone.now()
	if value.date() == now.date():
		time_str = value.strftime('%H:%M')
		if time_str.startswith('0'):
			time_str = time_str[1:]
		return 'Сегодня в {}'.format(time_str)
	elif value.date() == now.date() - timezone.timedelta(days=1):
		time_str = value.strftime('%H:%M')
		if time_str.startswith('0'):
			time_str = time_str[1:]
		return 'Вчера в {}'.format(time_str)
	else:
		return '{} {} {}'.format(value.day, months[value.month], value.strftime('%H:%M'))
