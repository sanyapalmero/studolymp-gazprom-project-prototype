from django.urls import path

from . import views

app_name = 'control'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('employees/', views.EmployessView.as_view(), name='employees'),
    path('employees/create-task/<int:pk>/', views.CreateTaskView.as_view(), name='create-task'),
    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path('tasks/accept/<int:pk>/', views.AcceptTaskView.as_view(), name='accept-task'),
    path('tasks/finish/<int:pk>/', views.FinishTaskView.as_view(), name='finish-task'),
]
