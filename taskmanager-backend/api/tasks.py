from celery import shared_task
from django.utils import timezone
from .models import *


@shared_task
def check_deadlines():
    now = timezone.now()
    overdue_tasks = Task.objects.filter(due_date__lte=now, is_completed=False)

    for task in overdue_tasks:
        # Здесь можно отправить уведомление (например, через Telegram бота)
        print(f"[!] Задача просрочена: {task.title}, Дедлайн: {task.due_date}")
        # send_telegram_notification.delay(task.user.telegram_id, f"Задача '{task.title}' просрочена!")

    return f"Проверено {overdue_tasks.count()} просроченных задач"
