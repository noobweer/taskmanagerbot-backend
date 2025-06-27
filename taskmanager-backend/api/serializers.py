from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    user = serializers.CharField(source='user.user')

    class Meta:
        model = Task
        fields = [
            'id',
            'created_date',
            'due_date',
            'title',
            'description',
            'is_completed',
            'category',
            'user',
        ]
        read_only_fields = ['id', 'created_date']


class TelegramLoginSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(min_value=1)

    def validate(self, data):
        telegram_id = data.get('telegram_id')
        if not isinstance(telegram_id, int) or telegram_id <= 0:
            raise serializers.ValidationError("Неверный формат Telegram ID")
        return data

    class Meta:
        model = User
        fields = ['telegram_id']