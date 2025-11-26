from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Task, Note, Reminder
from django.contrib.auth.forms import PasswordChangeForm
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
    class Meta:
        model = Task
        fields = ['title', 'description', 'subject', 'due_date', 'priority', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add details'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject (optional)'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


# ----------------------------
# Note Form
# ----------------------------
class NoteForm(forms.ModelForm):
    """Form for creating and updating notes"""
    
    class Meta:
        model = Note
        # user will be set from request.user in the view, don't expose it on the form
        fields = ['title', 'content', 'subject', 'tags']
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

class UserProfileForm(forms.ModelForm):
    """
    Form for editing user's profile information, including bio and profile picture.
    """
    
    # Custom fields based on your model: full_name is CharField, bio is TextField
    # Theme is a ChoiceField on the model, so we can render it naturally.

    class Meta:
        model = User
        # Fields that will be managed by the ModelForm
        fields = ['full_name', 'email', 'bio', 'profile_pic', 'theme'] 
        
        # We can explicitly define the widget for 'bio' to make it a textarea
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us a little bit about yourself...'}),
        }
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Fields to apply general text input styling
        text_input_fields = ['full_name', 'email']
        for field_name in text_input_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-input', 
                    'placeholder': self.fields[field_name].label
                })
        
        # Apply select styling to the theme field
        if 'theme' in self.fields:
            self.fields['theme'].widget.attrs.update({
                'class': 'form-select',
            })
            
        # Apply styling and placeholder to bio field
        if 'bio' in self.fields:
            self.fields['bio'].widget.attrs.update({
                'class': 'form-textarea',
            })
        
        # Customize the profile picture field's label
        if 'profile_pic' in self.fields:
             self.fields['profile_pic'].label = "Change Profile Picture"


class AdminCreationForm(forms.Form):
    """Form for creating a new admin account"""
    full_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition',
            'placeholder': 'Full Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition',
            'placeholder': 'admin@example.com'
        })
    )
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition',
            'placeholder': 'Confirm Password'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password1