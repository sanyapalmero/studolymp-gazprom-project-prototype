from django.urls import path

from . import views

app_name = 'control'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('employees/', views.EmployessView.as_view(), name='employees'),
    path('employees/create-task/<int:pk>/', views.CreateTaskView.as_view(), name='create-task'),
]
