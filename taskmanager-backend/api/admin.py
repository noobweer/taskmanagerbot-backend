from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'created_date',
        'due_date',
        'title',
        'short_description',
        'is_completed',
        'category',
        'user'
    )

    ordering = ['-created_date']

    def short_description(self, obj):
        return obj.description[:10] + '...' if obj.description and len(obj.description) > 10 else obj.description


admin.site.register(Category)
