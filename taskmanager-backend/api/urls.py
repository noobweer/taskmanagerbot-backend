from django.urls import path
from .views import *

urlpatterns = [
    path('telegram-login/', TelegramLoginView.as_view(), name='telegram-login'),
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('create-task/', CreateTaskView.as_view(), name='create-task'),
    path('edit-task/', EditTaskView.as_view(), name='edit-task'),
    path('delete-task/', DeleteTaskView.as_view(), name='delete-task'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('create-category/', CreateCategoryView.as_view(), name='create-category'),
    path('edit-category/', EditCategoryView.as_view(), name='edit-category'),
    path('delete-category/', DeleteCategoryView.as_view(), name='delete-category'),
]
