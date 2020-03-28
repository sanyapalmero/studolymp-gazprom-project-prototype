from django.utils.decorators import method_decorator
from django.views import generic

from users.decorators import login_required
from users.models import User


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
