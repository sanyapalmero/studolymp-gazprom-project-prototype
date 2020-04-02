from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=User.ROLE_ADMIN
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    ROLE_ADMIN = 'admin'
    ROLE_EMPLOYER = 'employer'
    ROLE_EMPLOYEE = 'employee'
    ROLE_CHOICES = [
        (ROLE_ADMIN, "Администратор"),
        (ROLE_EMPLOYER, "Руководство"),
        (ROLE_EMPLOYEE, "Сотрудник")
    ]

    email = models.EmailField(unique=True, max_length=255, verbose_name="Email")
    username = models.CharField(unique=False, max_length=255, verbose_name="Имя")
    role = models.CharField(max_length=64, choices=ROLE_CHOICES, default=ROLE_EMPLOYEE, verbose_name="Роль")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    # This field for users with role=ROLE_EMPLOYEE, for saving employer.
    employer = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="employees", verbose_name="Руководитель"
    )

    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_employer(self):
        return self.role == self.ROLE_EMPLOYER

    @property
    def is_employee(self):
        return self.role == self.ROLE_EMPLOYEE

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def all_tasks_count(self):
        if self.is_employee:
            return self.employee_task_set.count()
        elif self.is_employer:
            return self.employer_task_set.count()

    @property
    def waiting_tasks_count(self):
        from control.models import Task
        return self.employee_task_set.filter(status=Task.STATUS_WAITING).count()

    @property
    def working_tasks_count(self):
        from control.models import Task
        return self.employee_task_set.filter(status=Task.STATUS_WORKING).count()

    @property
    def finished_tasks_count(self):
        from control.models import Task
        return self.employee_task_set.filter(status=Task.STATUS_FINISHED).count()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
