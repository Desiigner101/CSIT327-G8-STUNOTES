from django.urls import path
from . import views

app_name = 'stunotes'   # 👈 this is important so {% url 'stunotes:login' %} works

urlpatterns = [
    # Auth routes
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # You can also add your home/dashboard
    path('', views.home, name='home'),
]
