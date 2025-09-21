from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Task URLs
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    
    # Note URLs
    path('notes/', views.note_list, name='note_list'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/<int:pk>/edit/', views.edit_note, name='edit_note'),
    path('notes/<int:pk>/delete/', views.delete_note, name='delete_note'),
    
    # User profile
    path('profile/', views.profile, name='profile'),
]