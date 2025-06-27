from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .services.category_service import CategoryService
from .services.task_service import TaskService
from .services.telegram_service import TelegramService
# Create your views here.


class TelegramLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = request.query_params

        login_result = TelegramService().login_telegram(data)
        return Response(login_result)


class TasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        tasks_result = TaskService().tasks(user)
        return Response(tasks_result)


class CreateTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        create_result = TaskService().create_task(data, user)
        return Response(create_result)


class EditTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        edit_result = TaskService().edit_task(data, user)
        return Response(edit_result)


class DeleteTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        delete_result = TaskService().delete_task(data, user)
        return Response(delete_result)


class CategoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        categories_result = CategoryService().categories()
        return Response(categories_result)


class CreateCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        create_result = CategoryService().create_category(data)
        return Response(create_result)


class EditCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        edit_result = CategoryService().edit_category(data)
        return Response(edit_result)


class DeleteCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        delete_result = CategoryService().delete_category(data)
        return Response(delete_result)
