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

]
