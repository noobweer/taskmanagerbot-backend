from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .services.category_service import CategoryService
from .services.task_service import TaskService
# Create your views here.


class CreateCategoryView(APIView):
    def post(self, request):
        data = request.data

        create_result = CategoryService().create_category(data)
        return Response(create_result)


class EditCategoryView(APIView):
    def post(self, request):
        data = request.data

        edit_result = CategoryService().edit_category(data)
        return Response(edit_result)


class DeleteCategoryView(APIView):
    def post(self, request):
        data = request.data

        delete_result = CategoryService().delete_category(data)
        return Response(delete_result)


class CreateTaskView(APIView):
    def post(self, request):
        data = request.data

        create_result = TaskService().create_task(data)
        return Response(create_result)


class EditTaskView(APIView):
    def post(self, request):
        data = request.data

        edit_result = TaskService().edit_task(data)
        return Response(edit_result)


class DeleteTaskView(APIView):
    def post(self, request):
        data = request.data

        delete_result = TaskService().delete_task(data)
        return Response(delete_result)
