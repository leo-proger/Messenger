# Messenger

This is a simple messenger on Django, Bootstrap 5 and channels. It's not done and won't be.

## Features

- Messaging in real time
- Unread messages
- Profile
- Edit profile (not completed)

## How to run

- Clone repository
- Go to project dir
- Run `pip install -r requirements.txt`
- Create `.env` file
- Put in .env `SECRET_KEY=your_secret_key` (you need to generate `SECRET_KEY` -
  `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- Put in .env `DEBUG=True`
- Run `python manage.py makemigration`
- Run `python manage.py migrate`
- Run redis on 6379 port (you can do it via Docker)
- Run `python manage.py runserver 8000`


