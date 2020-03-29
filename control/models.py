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
