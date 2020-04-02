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
    path('tasks/detail/<int:pk>/', views.DetailTaskView.as_view(), name='detail-task'),
    path('tasks/detail/<int:pk>/add-report/', views.AddReportView.as_view(), name='add-report'),
    path('tasks/detail/<int:pk>/remove-report/<int:file_pk>/', views.RemoveReportView.as_view(), name='remove-report'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
