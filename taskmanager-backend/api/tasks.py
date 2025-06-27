import requests
from celery import shared_task
from django.utils import timezone
from .models import *

# NOTE: move to env var
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_API_URL = f"https://api.telegram.org/bot {TELEGRAM_BOT_TOKEN}/sendMessage"


@shared_task
def check_deadlines():
    now = timezone.now()
    overdue_tasks = Task.objects.filter(due_date__lte=now, is_completed=False)

    for task in overdue_tasks:
        try:
            telegram_user = task.user.telegramuser
            message = f"⏰ Просроченная задача: {task.title}\nДедлайн: {task.due_date}"
            send_telegram_notification.delay(telegram_user.telegram_id, message)
        except Exception as e:
            print(e)
            continue

    return f"Проверено {overdue_tasks.count()} задач"


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def send_telegram_notification(telegram_id, message_text):
    payload = {
        "chat_id": telegram_id,
        "text": message_text
    }
    response = requests.post(TELEGRAM_API_URL, json=payload)

    if not response.ok:
        raise Exception(f"Ошибка отправки в Telegram: {response.text}")
