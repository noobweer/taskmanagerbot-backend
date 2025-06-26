from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from .services.ulid_service import ULIDField

# Create your models here.


class TelegramUser(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    telegram_id = models.BigIntegerField(unique=True)


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    id = ULIDField()
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    due_date = models.DateTimeField(null=False)
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=False)
    user = models.ForeignKey(TelegramUser, on_delete=models.PROTECT, null=False)

    def __str__(self):
        return f"{self.title} — Выполнено: {self.is_completed}, Категория: {self.category}, Юзер: {self.user}"