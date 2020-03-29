from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'for_user', 'from_user', 'created_at', 'status', 'until_to', 'finished_at')
