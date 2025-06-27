import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
AUTH_URL = "http://taskmanager-backend:8000/api/telegram-login/"
HEADERS = {"Content-Type": "application/json"}
