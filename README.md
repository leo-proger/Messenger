<h1 align="center">💬 Messenger</h1>

<p align="center">
  A web messenger built with Django, featuring real-time messaging.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" alt="Python 3.11">
  <img src="https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white" alt="Django 4.2">
  <img src="https://img.shields.io/badge/Channels-4.3-092E20?logo=django&logoColor=white" alt="Django Channels">
  <img src="https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white" alt="Bootstrap 5">
  <img src="https://img.shields.io/badge/WebSocket-realtime-010101?logo=socketdotio&logoColor=white" alt="WebSocket">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
</p>

> **I wrote this project when I was 13 — entirely on my own, without any AI Agent.**
> The code is a learning project and naive in places, but it works "live" over WebSocket.

> The project is unfinished and won't be developed further — it stays here as a keepsake and an example.

---

## Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/126c33d9-d34c-4f9f-854a-901088f90163" alt="Messenger — chat interface" width="900">
</p>

## Features

- **Real-time messaging** — delivered over WebSocket (Django Channels + Redis), no page reloads.
- **Online status** — track user presence and last-seen time.
- **Unread messages** — indicators for new messages in chats.
- **User profiles** — avatar, bio, city, age, phone number.
- **Email authentication** — custom user model instead of the default one.
- **Posts** — publish text and images on a profile.
- **Profile editing** *(work in progress)*.

## Tech Stack

| Category        | Technologies                                          |
| --------------- | ----------------------------------------------------- |
| Backend         | Python 3.11, Django 4.2                               |
| Real-time       | Django Channels, channels-redis, Daphne (ASGI), Redis |
| Frontend        | Django Templates, Bootstrap 5, Font Awesome           |
| Database        | SQLite (default)                                      |
| Media & utils   | Pillow, django-resized, django-phonenumber-field      |
| Configuration   | python-decouple (`.env`)                              |

## Getting Started

> Requires Python 3.11+ and Redis.

1. **Clone the repository and enter the project folder**
   ```bash
   git clone https://github.com/leo-proger/Messenger.git
   cd Messenger
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Generate a `SECRET_KEY` and put it into `.env`:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Start Redis on port 6379** (e.g. via Docker)
   ```bash
   docker run -p 6379:6379 redis
   ```

6. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Run the server**
   ```bash
   python manage.py runserver 8000
   ```

   The app will be available at [http://localhost:8000](http://localhost:8000).

## Project Structure

```
Messenger/
├── app/        # Project configuration (settings, asgi, routing, urls)
├── chats/      # Chats and messages: models, WebSocket consumers, signals
├── users/      # Users, profiles, posts, online status
├── templates/  # HTML templates (Bootstrap 5)
├── static/     # Static assets: CSS, JS, images
└── media/      # User-uploaded files
```

## License

This project is licensed under the [MIT License](LICENSE).
