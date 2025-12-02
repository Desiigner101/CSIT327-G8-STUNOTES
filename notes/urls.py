from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    #Home
    path('', views.landing_view, name='landing'),
    path('landing/', views.landing_view, name='landing_page'),
    path('home/', views.home, name='home'),
    
    #Settings
    path('settings/', views.settings_page, name='settings_page'),
    path('delete-account/', views.delete_account, name='delete_account'),
    
    # Note creation
    path('add_note/', views.add_note, name='add_note'),
    path('note/edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('note/delete/<int:note_id>/', views.delete_note, name='delete_note'),

    #Login and Register URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    #Task URLs
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('toggle/<int:task_id>/', views.toggle_task_status, name='toggle_task_status'),
    
    #Profile URLs
    path('profile/', views.profile_view, name='profile_view'), 
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Notes list
    path('notes/', views.notes_list, name='notes_list'),

    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-user/', views.add_user, name='add_user'),  # ✅ Added earlier
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),  # ✅ ADD THIS LINE
    path('switch-to-user/', views.switch_to_user_mode, name='switch_to_user_mode'),
    path('switch-to-admin/', views.switch_to_admin_mode, name='switch_to_admin_mode'),
    
    # Calendar
    path('calendar/', views.calendar_view, name='calendar'),
]