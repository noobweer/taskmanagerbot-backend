import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
AUTH_URL = "http://taskmanager-backend:8000/api/telegram-login/"
TASK_URL = "http://taskmanager-backend:8000/api/tasks/"
CREATE_TASK_URL = "http://taskmanager-backend:8000/api/create-task/"
HEADERS = {"Content-Type": "application/json"}
