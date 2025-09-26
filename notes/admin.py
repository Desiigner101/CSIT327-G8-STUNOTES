from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Task, Note, Reminder

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for the User model.

    Customizes how User instances appear in the Django admin interface.
    Displays full_name instead of first_name/last_name and includes StuNotes-specific fields.
    """
    # Filters available in the right sidebar
    list_filter = ['is_superuser', 'is_staff', 'theme', 'notifications_enabled', 'created_at']
    
    # Fields that can be searched
    search_fields = ['username', 'full_name', 'email']
    
    # Default ordering in list view
    ordering = ['-created_at']
    
    # Fieldsets for editing existing users
    fieldsets = BaseUserAdmin.fieldsets + (
        ('StuNotes Profile', {
            'fields': ('full_name', 'bio', 'profile_pic', 'theme', 'notifications_enabled')
        }),
    )
    
    # Fieldsets for adding a new user
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('StuNotes Profile', {
            'fields': ('full_name', 'bio', 'profile_pic', 'theme', 'notifications_enabled')
        }),
    )

    # Force list_display to show full_name
    def get_list_display(self, request):
        return ['username', 'full_name', 'email', 'is_admin', 'created_at', 'is_superuser', 'is_staff']

    class Media:
        css = {'all': ('admin_assets/css/admin.css',)}
        js = ('admin_assets/js/admin.js',)

# -------------------------
# Other admin classes remain the same
# -------------------------

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'subject', 'priority', 'status', 'due_date', 'created_at']
    list_filter = ['priority', 'status', 'subject', 'created_at', 'due_date']
    search_fields = ['title', 'user__username', 'subject', 'description']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Task Information', {
            'fields': ('user', 'title', 'description', 'subject')
        }),
        ('Task Details', {
            'fields': ('due_date', 'priority', 'status')
        }),
    )
    
    class Media:
        css = {'all': ('admin_assets/css/admin.css',)}
        js = ('admin_assets/js/admin.js',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'subject', 'created_at']
    list_filter = ['subject', 'created_at']
    search_fields = ['title', 'user__username', 'content', 'subject', 'tags']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Note Information', {
            'fields': ('user', 'title', 'subject')
        }),
        ('Content', {
            'fields': ('content', 'tags')
        }),
    )
    
    class Media:
        css = {'all': ('admin_assets/css/admin.css',)}
        js = ('admin_assets/js/admin.js',)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['task', 'remind_time', 'is_sent', 'created_at']
    list_filter = ['is_sent', 'remind_time', 'created_at']
    search_fields = ['task__title', 'task__user__username']
    ordering = ['remind_time']
    
    fieldsets = (
        ('Reminder Details', {
            'fields': ('task', 'remind_time', 'is_sent')
        }),
    )
    
    class Media:
        css = {'all': ('admin_assets/css/admin.css',)}
        js = ('admin_assets/js/admin.js',)


# Customize the admin site headers and titles
admin.site.site_header = "StuNotes Administration"
admin.site.site_title = "StuNotes Admin Portal"
admin.site.index_title = "Welcome to StuNotes Administration"
