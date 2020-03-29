from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic

from users.decorators import login_required
from users.models import User

from .forms import TaskForm
from .models import Task


class HomeView(generic.TemplateView):
    template_name = 'control/home.html'


@method_decorator(login_required, name='dispatch')
class EmployessView(generic.ListView):
    template_name = 'control/employees.html'
    model = User
    paginate_by = 20

    def get_queryset(self):
        queryset = self.model.objects.filter(role=User.ROLE_EMPLOYEE, employer=self.request.user)
        return queryset


@method_decorator(login_required, name='dispatch')
class CreateTaskView(generic.CreateView):
    template_name = 'control/employees.html'

    def post(self, request, pk):
        task_form = TaskForm(request.POST)
        object_list = User.objects.filter(role=User.ROLE_EMPLOYEE, employer=request.user)
        if task_form.is_valid():
            for_user = get_object_or_404(User, pk=pk)
            Task.objects.create(
                for_user=for_user,
                from_user=request.user,
                text=task_form.cleaned_data["text"],
                until_to=task_form.cleaned_data["until_to"],
            )
            return render(request, self.template_name, {
                "task_created": "Задача успешно отправлена сотруднику",
                "object_list": object_list
            })
        else:
            return render(request, self.template_name, {
                "modal_show": pk,
                "task_form": task_form,
                "object_list": object_list
            })


@method_decorator(login_required, name='dispatch')
class TasksView(generic.ListView):
    template_name = 'control/tasks.html'
    model = Task
    paginate_by = 20

    def get_context_data(self):
        context = super(TasksView, self).get_context_data()
        employee_pk = self.request.GET.get("employee")
        if employee_pk:
            employee = get_object_or_404(User, pk=employee_pk)
            context["employee"] = employee
        return context

    def get_queryset(self):
        queryset = self.model.objects.all()

        if self.request.user.is_employer:
            employee_pk = self.request.GET.get("employee")

            if not employee_pk:
                return queryset.none()

            for_user = get_object_or_404(User, pk=employee_pk)
            return self.model.objects.filter(for_user=for_user, from_user=self.request.user)
        elif self.request.user.is_employee:
            return self.model.objects.filter(for_user=self.request.user)


@method_decorator(login_required, name='dispatch')
class AcceptTaskView(generic.View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.user.is_employee and task.for_user == request.user:
            task.status = Task.STATUS_WORKING
            task.save()
            return redirect(reverse("control:tasks"))
        else:
            logout(request)
            return redirect(reverse("users:login"))


@method_decorator(login_required, name='dispatch')
class FinishTaskView(generic.View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.user.is_employee and task.for_user == request.user:
            task.status = Task.STATUS_FINISHED
            task.finished_at = timezone.now()
            task.save()
            return redirect(reverse("control:tasks"))
        else:
            logout(request)
            return redirect(reverse("users:login"))


@method_decorator(login_required, name='dispatch')
class DetailTaskView(generic.DetailView):
    template_name = 'control/task-detail.html'

    def get_object(self):
        task = get_object_or_404(Task, pk=self.kwargs.get("pk"))
        return task
