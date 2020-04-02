# Generated by Django 3.0.3 on 2020-04-01 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0003_task_file_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskfile',
            name='file_type',
            field=models.CharField(choices=[('report', 'Отчёт'), ('task_addon', 'Дополнение к задаче')], default='task_addon', max_length=10),
        ),
    ]