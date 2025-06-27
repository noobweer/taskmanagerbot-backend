from django.urls import path
from .views import *

urlpatterns = [
    path('telegram-login/', TelegramLoginView.as_view(), name='telegram-login'),
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('create-task/', CreateTaskView.as_view(), name='create-task')
]
