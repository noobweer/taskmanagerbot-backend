import os
import logging
import requests
from celery import shared_task
from django.utils import timezone
from .models import *

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


@shared_task
def check_deadlines():
    now = timezone.now()
    overdue_tasks = Task.objects.filter(due_date__lte=now, is_completed=False)

    for task in overdue_tasks:
        try:
            telegram_user = task.user

            message = f"⏰ Просроченная задача: {task.title}\nДедлайн: {task.due_date}"
            send_telegram_notification.delay(telegram_user.telegram_id, message)
        except Exception as e:
            logger.warning(f"Ошибка при обработке задачи {task.id}: {e}")
            continue

    return f"Проверено {overdue_tasks.count()} задач"


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def send_telegram_notification(telegram_id, message_text):
    payload = {
        "chat_id": int(telegram_id),
        "text": message_text
    }
    headers = {"Content-Type": "application/json"}

    logger.info(f"Отправка уведомления в Telegram ID={telegram_id}: {message_text}")

    response = requests.post(TELEGRAM_API_URL, json=payload, headers=headers)

    logger.info(f"Ответ Telegram: {response.status_code}, {response.text}")

    if not response.ok:
        raise Exception(f"Ошибка отправки в Telegram: {response.text}")

