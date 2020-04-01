from django.contrib import admin

from .models import Task, TaskFile


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'for_user', 'from_user', 'created_at', 'status', 'until_to', 'finished_at')


@admin.register(TaskFile)
class TaskFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'file', 'file_type')
