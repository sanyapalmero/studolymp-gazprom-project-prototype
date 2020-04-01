import os
import secrets

from django.db import models

from users.models import User


class Task(models.Model):
    STATUS_WAITING = 'waiting'
    STATUS_WORKING = 'working'
    STATUS_FINISHED = 'finished'
    STATUS_CHOICES = [
        (STATUS_WAITING, "Ожидает принятия"),
        (STATUS_WORKING, "В работе"),
        (STATUS_FINISHED, "Завершено")
    ]

    for_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_task_set")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employer_task_set")

    text = models.TextField(verbose_name="Описание задачи")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=STATUS_WAITING, verbose_name="Статус")

    until_to = models.DateTimeField(verbose_name="Сроком до")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    finished_at = models.DateTimeField(verbose_name="Дата завершения", null=True, blank=True)

    @property
    def is_waiting(self):
        return self.status == self.STATUS_WAITING

    @property
    def is_working(self):
        return self.status == self.STATUS_WORKING

    @property
    def is_finished(self):
        return self.status == self.STATUS_FINISHED

    @property
    def files(self):
        return self.taskfile_set.filter(file_type=TaskFile.TYPE_TASK_ADDON)

    @property
    def reports(self):
        return self.taskfile_set.filter(file_type=TaskFile.TYPE_REPORT)


def get_file_path(user, filename):
    secret_path = secrets.token_hex(32)
    return os.path.join("task-files", secret_path, filename)


class TaskFile(models.Model):
    TYPE_REPORT = "report"
    TYPE_TASK_ADDON = "task_addon"
    TYPE_CHOICES = [
        (TYPE_REPORT, "Отчёт"),
        (TYPE_TASK_ADDON, "Дополнение к задаче")
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_file_path, verbose_name="Файл")
    title = models.CharField(max_length=64, verbose_name="Название файла")
    file_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_TASK_ADDON)
