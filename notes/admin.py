from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Task, Note, Reminder

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_admin', 'created_at', 'is_superuser', 'is_staff']
    list_filter = ['is_superuser', 'is_staff', 'theme', 'notifications_enabled', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    # Add custom fields to the user form
    fieldsets = BaseUserAdmin.fieldsets + (
        ('StuNotes Profile', {
            'fields': ('bio', 'profile_pic', 'is_admin', 'theme', 'notifications_enabled')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('StuNotes Profile', {
            'fields': ('bio', 'profile_pic', 'is_admin', 'theme', 'notifications_enabled')
        }),
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for Task model"""
    list_display = ['title', 'user', 'subject', 'priority', 'status', 'due_date', 'created_at']
    list_filter = ['priority', 'status', 'subject', 'created_at', 'due_date']
    search_fields = ['title', 'user__username', 'subject', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Task Information', {
            'fields': ('user', 'title', 'description', 'subject')
        }),
        ('Task Details', {
            'fields': ('due_date', 'priority', 'status')
        }),
    )

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Admin configuration for Note model"""
    list_display = ['title', 'user', 'subject', 'created_at']
    list_filter = ['subject', 'created_at']
    search_fields = ['title', 'user__username', 'content', 'subject', 'tags']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Note Information', {
            'fields': ('user', 'title', 'subject')
        }),
        ('Content', {
            'fields': ('content', 'tags')
        }),
    )

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    """Admin configuration for Reminder model"""
    list_display = ['task', 'remind_time', 'is_sent', 'created_at']
    list_filter = ['is_sent', 'remind_time', 'created_at']
    search_fields = ['task__title', 'task__user__username']
    ordering = ['remind_time']
    date_hierarchy = 'remind_time'
    
    fieldsets = (
        ('Reminder Details', {
            'fields': ('task', 'remind_time', 'is_sent')
        }),
    )

# Customize admin site
admin.site.site_header = "StuNotes Administration"
admin.site.site_title = "StuNotes Admin Portal"
admin.site.index_title = "Welcome to StuNotes Administration"