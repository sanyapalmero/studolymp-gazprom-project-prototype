from django.shortcuts import get_object_or_404, redirect, render, reverse
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
class CreateTask(generic.CreateView):
    template_name = 'control/employees.html'

    def post(self, request, pk):
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            for_user = get_object_or_404(User, pk=pk)
            Task.objects.create(
                for_user=for_user,
                from_user=request.user,
                text=task_form.cleaned_data["text"],
                until_to=task_form.cleaned_data["until_to"],
            )
            return redirect(reverse("control:employees"))
        else:
            object_list = User.objects.filter(role=User.ROLE_EMPLOYEE, employer=request.user)
            return render(request, self.template_name, {
                "modal_show": pk,
                "task_form": task_form,
                "object_list": object_list
            })
