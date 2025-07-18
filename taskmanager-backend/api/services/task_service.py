from datetime import datetime
from django.utils import timezone

from ..models import *
from ..serializers import TaskSerializer


class TaskService:
    def __init__(self):
        self.Task = Task.objects
        self.Category = Category.objects
        self.TelegramUser = TelegramUser.objects

    def create_task(self, data, user):
        try:
            due_date_str = data.get('due_date')  #example datetime 2025-04-05T14:30:00
            title = data.get('title')
            description = data.get('description')
            category_name = data.get('category')
            user_obj = self.TelegramUser.get(user=user)

            if not all([due_date_str, title, category_name]):
                return {'is_created': False,
                        'message': 'Send all required fields (due_date, title, category)'}

            try:
                due_date = datetime.fromisoformat(due_date_str)
                if timezone.is_naive(due_date):
                    due_date = timezone.make_aware(due_date)
            except ValueError:
                return {
                    'is_edited': False,
                    'message': f'Invalid date format for due_date: {due_date_str}. Use ISO 8601 format.'
                }

            if due_date < timezone.now():
                return {
                    'is_created': False,
                    'message': f'Due date cannot be in the past: {due_date_str}'
                }

            if not self.Category.filter(name=category_name).exists():
                return {'is_created': False, 'message': f'Invalid category: {category_name}'}
            category_obj = self.Category.get(name=category_name)

            self.Task.create(due_date=due_date, title=title, description=description,
                             category=category_obj, user=user_obj)
            return {'is_created': True, 'message': f'Task created successfully'}
        except Exception as e:
            return {'is_created': False, 'message': str(e)}

    def edit_task(self, data, user):
        try:
            task_id = data.get('id')
            due_date_str = data.get('due_date')  #example datetime 2025-04-05T14:30:00
            title = data.get('title')
            description = data.get('description')
            category_name = data.get('category')
            is_completed = data.get('is_completed')
            user_obj = self.TelegramUser.get(user=user)

            if not all([task_id, due_date_str, title, category_name]):
                return {'is_edited': False,
                        'message': 'Send all required fields (task_id, due_date, title, category_name, is_completed)'}

            if not self.Task.filter(id=task_id, user=user_obj).exists():
                return {'is_edited': False, 'message': f'Invalid id of the task or user: {task_id}, {user_obj}'}
            task_obj = self.Task.get(id=task_id, user=user_obj)

            try:
                due_date = datetime.fromisoformat(due_date_str)
            except ValueError:
                return {
                    'is_edited': False,
                    'message': f'Invalid date format for due_date: {due_date_str}. Use ISO 8601 format.'
                }

            if due_date < timezone.now():
                return {
                    'is_edited': False,
                    'message': f'Due date cannot be in the past: {due_date_str}'
                }

            if not self.Category.filter(name=category_name).exists():
                return {'is_edited': False, 'message': f'Invalid category: {category_name}'}
            category_obj = self.Category.get(name=category_name)

            if not isinstance(is_completed, bool):
                return {'is_edited': False, 'message': f'Invalid is_completed: {is_completed}'}

            task_obj.due_date = due_date
            task_obj.title = title
            task_obj.description = description
            task_obj.category = category_obj
            task_obj.user = user_obj
            task_obj.is_completed = is_completed
            task_obj.save()
            return {'is_edited': True, 'message': f'Task edited successfully'}
        except Exception as e:
            return {'is_edited': False, 'message': str(e)}

    def delete_task(self, data, user):
        try:
            task_id = data.get('id')
            user_obj = self.TelegramUser.get(user=user)

            if not all([task_id]):
                return {'is_deleted': False,
                        'message': 'Send all required fields (task_id)'}

            if not self.Task.filter(id=task_id).exists():
                return {'is_deleted': False, 'message': f'Invalid id of the task: {task_id}'}

            self.Task.get(id=task_id, user=user_obj).delete()
            return {'is_deleted': True, 'message': f'Task deleted successfully'}
        except Exception as e:
            return {'is_deleted': False, 'message': str(e)}

    def tasks(self, user):
        try:
            user_obj = self.TelegramUser.get(user=user)
            tasks = self.Task.filter(user=user_obj)
            serializer = TaskSerializer(tasks, many=True)

            return {'success': True, 'tasks': serializer.data, 'message': 'Fetched tasks successfully'}
        except Exception as e:
            return {'success': False, 'tasks': [], 'message': str(e)}
