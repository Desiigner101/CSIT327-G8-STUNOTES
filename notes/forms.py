from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Task, Note, Reminder

# ----------------------------
# User Forms
# ----------------------------
class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new user with full_name and email"""
    class Meta:
        model = User
        fields = ['full_name', 'email', 'username', 'password1', 'password2', 'bio', 'profile_pic', 'theme', 'notifications_enabled']

class CustomUserChangeForm(UserChangeForm):
    """Form for updating existing user details"""
    class Meta:
        model = User
        fields = ['full_name', 'email', 'username', 'bio', 'profile_pic', 'theme', 'notifications_enabled']


# ----------------------------
# Task Form
# ----------------------------
class TaskForm(forms.ModelForm):
    """Form for creating and updating tasks"""
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )
    
    class Meta:
        model = Task
        fields = ['user', 'title', 'description', 'subject', 'due_date', 'priority', 'status']


# ----------------------------
# Note Form
# ----------------------------
class NoteForm(forms.ModelForm):
    """Form for creating and updating notes"""
    
    class Meta:
        model = Note
        fields = ['user', 'title', 'content', 'subject', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'tags': forms.TextInput(attrs={'placeholder': 'Comma-separated tags'}),
        }


# ----------------------------
# Reminder Form
# ----------------------------
class ReminderForm(forms.ModelForm):
    """Form for creating and updating reminders"""
    remind_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    class Meta:
        model = Reminder
        fields = ['task', 'remind_time', 'is_sent']
