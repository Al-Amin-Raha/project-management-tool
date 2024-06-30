# management/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/update/', views.update_project, name='update_project'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('projects/<int:project_id>/tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/update-status/', views.update_task_status, name='update_task_status'),

]
