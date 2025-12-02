from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Extended User model for StuNotes with full_name and email as login"""
    
    # Custom fields
    full_name = models.CharField(max_length=255, default="Unknown")  # Full name of the user
    email = models.EmailField(unique=True)  # Email used as login (must be unique)
    
    # Optional profile fields
    bio = models.TextField(max_length=500, blank=True)  # Short biography
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')  # Profile image
    
    # User interface preference
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='light')  # Light or dark mode
    notifications_enabled = models.BooleanField(default=True)  # Whether notifications are enabled
    
    # Admin configuration
    is_admin_only = models.BooleanField(
        default=False,
        help_text="If True, this admin account cannot access user features"
    )
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)  # Date of user creation
    updated_at = models.DateTimeField(auto_now=True)  # Date of last profile update
    
    # Authentication settings
    USERNAME_FIELD = 'email'  # Email is used for login
    REQUIRED_FIELDS = ['username', 'full_name']  # Fields required when creating a superuser
    
    def __str__(self):
        return self.full_name or self.email

    @property
    def is_admin(self):
        return self.is_superuser

    class Meta:
        db_table = 'notes_user'

    @property
    def profile_pic_url(self):
        """
        Return a safe URL for the user's profile picture. If the stored file
        is missing from storage, return the static default image path so
        templates don't raise when accessing `.url` on a missing file.
        """
        try:
            if self.profile_pic and getattr(self.profile_pic, 'name', None):
                # Check whether the file actually exists in storage
                storage = self.profile_pic.storage
                name = self.profile_pic.name
                if storage.exists(name):
                    return self.profile_pic.url
        except Exception:
            pass

        # Fallback to static default user icon (use existing asset)
        from django.conf import settings
        return f"{settings.STATIC_URL}notes/images/profile_pic.png"


class Task(models.Model):
    """Task model for managing student assignments"""
    
    # Priority levels for tasks
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    # Status options for tasks
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')  # Owner of the task
    title = models.CharField(max_length=200)  # Task title
    description = models.TextField(blank=True)  # Task details
    subject = models.CharField(max_length=100, blank=True)  # Optional subject/course
    due_date = models.DateTimeField(null=True, blank=True)  # Optional due date
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')  # Task priority
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')  # Task status
    created_at = models.DateTimeField(default=timezone.now)  # Task creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp
    
    class Meta:
        ordering = ['-created_at']  # Default ordering: newest first
        db_table = 'notes_task'  # Custom database table name
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"  # Show task title and owner
    
    @property
    def is_overdue(self):
        # Returns True if the task is past due and not completed
        if self.due_date and self.status != 'completed':
            return timezone.now() > self.due_date
        return False


class Note(models.Model):
    """Note model for storing student notes"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')  # Owner of the note
    title = models.CharField(max_length=200)  # Note title
    content = models.TextField()  # Main note content
    subject = models.CharField(max_length=100, blank=True)  # Optional subject/course
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")  # Optional tags
    created_at = models.DateTimeField(default=timezone.now)  # Note creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp
    
    class Meta:
        ordering = ['-created_at']  # Default ordering: newest first
        db_table = 'notes_note'  # Custom database table name
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"  # Show note title and owner
    
    def get_tags_list(self):
        # Returns a list of tags, split by commas
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class Reminder(models.Model):
    """Reminder model for task notifications"""
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reminders')  # Linked task
    remind_time = models.DateTimeField()  # When the reminder should trigger
    is_sent = models.BooleanField(default=False)  # Whether the reminder has been sent
    created_at = models.DateTimeField(default=timezone.now)  # Creation timestamp
    
    class Meta:
        ordering = ['remind_time']  # Order reminders by upcoming time
        db_table = 'notes_reminder'  # Custom database table name
    
    def __str__(self):
        return f"Reminder for {self.task.title} at {self.remind_time}"  # Display reminder info
    
    @property
    def is_due(self):
        # Returns True if the reminder time has passed and it hasn't been sent
        return timezone.now() >= self.remind_time and not self.is_sent
