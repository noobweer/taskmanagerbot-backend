from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    username = serializers.CharField(source='user.username')

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
            'username',
        ]
        read_only_fields = ['id', 'created_date']
