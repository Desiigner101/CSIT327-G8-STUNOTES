from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    #Home
    path('', views.home, name='home'),

    #Login and Regiser URLs
     path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path("edit/<int:task_id>/", views.edit_task, name="edit_task"),
    path('profile/', views.profile_view, name='profile_view'), 
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
