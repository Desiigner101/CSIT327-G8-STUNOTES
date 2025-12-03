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
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'min': ''}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_due_date(self):
        """Validate that due_date is not in the past"""
        from django.utils import timezone
        due_date = self.cleaned_data.get('due_date')
        if due_date:
            now = timezone.now()
            # Compare dates (ignore microseconds for comparison)
            if due_date < now:
                raise forms.ValidationError("Due date cannot be in the past. Please select today or a future date.")
        return due_date


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

    def clean_profile_pic(self):
        """
        Validate uploaded profile image: file size and content type.
        Limits: <= 3 MB, image/* MIME types only.
        """
        pic = self.cleaned_data.get('profile_pic')
        if not pic:
            return pic

        # Size check (3 MB)
        max_bytes = 3 * 1024 * 1024
        try:
            size = getattr(pic, 'size', 0) or 0
            if size > max_bytes:
                raise forms.ValidationError("Profile image must be 3 MB or smaller.")
        except Exception:
            pass

        # Content type check
        content_type = getattr(getattr(pic, 'file', None), 'content_type', '') or getattr(pic, 'content_type', '')
        if content_type and not content_type.startswith('image/'):
            raise forms.ValidationError("Please upload a valid image file.")

        return pic

class AdminCreationForm(forms.Form):
    """Form for creating a new admin account or upgrading existing account"""
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
        }),
        help_text='Enter an existing email to upgrade that account to admin, or a new email to create a new admin account.'
    )
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition',
            'placeholder': 'Password'
        }),
        help_text='For existing users, this will become their new password.'
    )
    is_admin_only = forms.BooleanField(
        label='Admin-only account',
        required=False,
        initial=False,
        help_text='If checked, this admin account will be admin-only and not have regular user features (Notes/Tasks).'
    )
    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition',
            'placeholder': 'Confirm Password'
        })
    )
    
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


class UserCreationForm(forms.Form):
    """Form for creating a new regular user account"""
    full_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition',
            'placeholder': 'Full Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition',
            'placeholder': 'user@example.com'
        })
    )
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition',
            'placeholder': 'Confirm Password'
        })
    )
    
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
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email