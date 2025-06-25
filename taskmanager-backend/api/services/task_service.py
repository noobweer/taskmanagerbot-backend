from ..models import *
from django.contrib.auth.models import User


class TaskService:
    def __init__(self):
        self.Task = Task.objects
        self.Category = Category.objects

    def create_task(self, data):
        try:
            due_to_date = data.get('deadline')
            title = data.get('title')
            description = data.get('description')
            category_name = data.get('category')
            username = data.get('username')

            if not all([due_to_date, title, category_name, username]):
                return {'is_created': False,
                        'message': 'Send all required fields (due_to_date, title, category_name, username)'}

            if not self.Category.filter(name=category_name).exists():
                return {'is_created': False, 'message': f'Invalid category: {category_name}'}
            category_obj = self.Category.get(name=category_name)

            if not User.objects.filter(username=username).exists():
                return {'is_created': False, 'message': f'Invalid username: {username}'}

            self.Task.create()
            return {'is_created': True, 'message': f'Task created successfully'}
        except Exception as e:
            return {'is_created': False, 'message': str(e)}
