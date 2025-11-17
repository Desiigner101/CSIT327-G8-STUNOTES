from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.urls import reverse
from .models import Task, Note
from .forms import TaskForm, UserProfileForm, NoteForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Get the custom User model
User = get_user_model()

def register_view(request):
    """
    Handles user registration.
    """
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("notes:register")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists!")
            return redirect("notes:register")

        # Create the user
        user = User.objects.create_user(
            email=email,
            username=email,
            full_name=full_name,
            password=password1
        )

        messages.success(request, "Registration successful! Please log in.")
        return redirect("notes:login")

    return render(request, "register.html")


def login_view(request):
    """
    Handles user login.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("notes:home")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("notes:login")

    return render(request, "login.html")


@login_required
def home(request):
    """
    Render the home page with tasks, notes, and statistics.
    Handles task creation and editing.
    """
    user = request.user
    
    # Get all user tasks and notes
    tasks = Task.objects.filter(user=user).order_by('-created_at')
    notes = Note.objects.filter(user=user).order_by('-created_at')[:5]  # Latest 5 notes
    
    # ✅ Calculate task statistics
    total_tasks = tasks.count()
    completed_tasks_count = tasks.filter(status='completed').count()
    pending_tasks_count = tasks.filter(status='pending').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    
    # ✅ Calculate overdue tasks
    now = timezone.now()
    overdue_tasks_count = tasks.filter(
        due_date__lt=now, 
        status__in=['pending', 'in_progress']
    ).count()
    
    # ✅ Get today's active tasks (exclude completed)
    today = now.date()
    today_tasks = tasks.filter(
        due_date__date=today,
        status__in=['pending', 'in_progress']
    ).order_by('due_date')
    
    # ✅ Total notes count
    total_notes = Note.objects.filter(user=user).count()
    
    # ✅ Get completed tasks history
    completed_tasks_list = tasks.filter(status='completed').order_by('-updated_at')
    
    # ✅ Get pending tasks list
    pending_tasks_list = tasks.filter(status='pending').order_by('due_date')
    
    # ✅ Get overdue tasks list
    overdue_tasks_list = tasks.filter(
        due_date__lt=now,
        status__in=['pending', 'in_progress']
    ).order_by('due_date')
    
    # ✅ Get all notes list
    all_notes_list = Note.objects.filter(user=user).order_by('-created_at')
    
    # ✅ NEW: Get unique subjects for filter dropdown
    unique_subjects = Note.objects.filter(
        user=user, 
        subject__isnull=False
    ).exclude(
        subject=''
    ).values_list('subject', flat=True).distinct().order_by('subject')

    # ✅ Get upcoming tasks due within 24 hours
    from datetime import timedelta
    next_24h = now + timedelta(hours=24)
    upcoming_tasks = tasks.filter(
        due_date__gte=now,
        due_date__lte=next_24h,
        status__in=['pending', 'in_progress']
    ).order_by('due_date')
    
    # Detect if editing
    edit_task_id = request.GET.get("edit")
    task_to_edit = None
    edit_form = None

    if edit_task_id:
        task_to_edit = get_object_or_404(Task, id=edit_task_id, user=user)
        edit_form = TaskForm(instance=task_to_edit)

    # Handle POST requests (create or edit task)
    if request.method == "POST":
        if "edit_task_id" in request.POST:  # Editing existing task
            task_to_edit = get_object_or_404(Task, id=request.POST["edit_task_id"], user=user)
            form = TaskForm(request.POST, instance=task_to_edit)
            if form.is_valid():
                form.save()
                messages.success(request, "Task updated successfully!")
                return redirect("notes:home")
        else:  # Creating new task
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = user
                task.save()
                messages.success(request, "Task created successfully!")
                return redirect("notes:home")
    else:
        form = TaskForm()

    # ✅ Context with all stats data
    context = {
        # Show only active tasks (not completed) in the main task list
        'tasks': tasks.exclude(status='completed')[:10],
        'notes': notes,
        'form': form,
        'edit_form': edit_form,
        'task_to_edit': task_to_edit,
        
        # Stats for overview cards
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks_count,
        'pending_tasks': pending_tasks_count,
        'in_progress_tasks': in_progress_tasks,
        'overdue_tasks': overdue_tasks_count,
        'total_notes': total_notes,
        
        # Today's tasks for calendar
        'today_tasks': today_tasks,
        
        # Lists for modals
        'completed_tasks_list': completed_tasks_list,
        'pending_tasks_list': pending_tasks_list,
        'overdue_tasks_list': overdue_tasks_list,
        'all_notes_list': all_notes_list,
        'upcoming_tasks': upcoming_tasks,
        
        # NEW: Unique subjects for filter
        'unique_subjects': unique_subjects,
        
        # Dynamic sidebar counters
        'total_tasks_count': total_tasks,
        'total_notes_sidebar': total_notes,
    }

    return render(request, "home.html", context)



def logout_view(request):
    """
    Logs out the current user and redirects to login page.
    """
    logout(request)
    messages.success(request, "You have logged out!")
    return redirect("notes:login")

@login_required
def toggle_task_status(request, task_id):
    """
    Toggle task status between completed and pending.
    """
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == "POST":
        if task.status == 'completed':
            task.status = 'pending'
            messages.success(request, f"Task '{task.title}' marked as incomplete!")
        else:
            task.status = 'completed'
            task.updated_at = timezone.now()  # Update the completion time
            messages.success(request, f"Task '{task.title}' marked as complete! 🎉")
        
        task.save()
    
    return redirect('notes:home')

@login_required
def delete_task(request, task_id):
    """
    Deletes a task belonging to the logged-in user.
    """
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('notes:home')
    return redirect('notes:home')


@login_required
def edit_task(request, task_id):
    """
    Handles editing a task.
    """
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('notes:home')
    else:
        form = TaskForm(instance=task)

    return render(request, "edit_task.html", {"form": form, "task": task})


@login_required
def profile_view(request):
    """
    Renders the user's profile page and calculates user statistics.
    """
    user = request.user
    
    # Calculate Task Statistics
    total_tasks = Task.objects.filter(user=user).count()
    completed_tasks = Task.objects.filter(user=user, status='completed').count()
    
    # Calculate Note Statistics
    total_notes = Note.objects.filter(user=user).count()
    
    context = {
        'user': user,
        'total_notes_created': total_notes,
        'total_tasks_created': total_tasks,
        'tasks_completed': completed_tasks,
    }
    return render(request, 'profile_view.html', context)


@login_required
def edit_profile(request):
    """
    Handles displaying and processing the User Profile edit form.
    """
    user = request.user
    
    if request.method == "POST":
        # Accept first_name and last_name from the form even though the ModelForm
        # still manages full_name. We'll compose full_name from the two fields
        # and set first_name/last_name on the user instance before saving.
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        # Initialize the form with posted data
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            # Prepare instance without committing so we can set extras
            profile = form.save(commit=False)
            # If a new profile picture was uploaded, remove the old file to save space
            # but avoid deleting the project's default placeholder image.
            if 'profile_pic' in request.FILES:
                try:
                    old = User.objects.get(pk=user.pk).profile_pic
                except User.DoesNotExist:
                    old = None
                if old and getattr(old, 'name', None) and old.name != 'default.jpg':
                    try:
                        old.delete(save=False)
                    except Exception:
                        # If deletion fails (e.g., storage not writable), continue silently
                        pass
            # Set first_name/last_name and ensure full_name is consistent
            profile.first_name = first_name
            profile.last_name = last_name
            # If full_name provided via hidden field, prefer it; otherwise compose
            full_from_post = request.POST.get('full_name', '').strip()
            if full_from_post:
                profile.full_name = full_from_post
            else:
                profile.full_name = (first_name + (' ' + last_name if first_name and last_name else '')).strip() or profile.full_name

            profile.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("notes:profile_view")
        else:
            messages.error(request, "Please correct the errors below.")
            
    else:
        # If the user doesn't have first_name/last_name populated but has
        # a `full_name`, split it for a better UX so the form shows the
        # name split across the two fields instead of all in `first_name`.
        initial = {}
        if (not user.first_name or not user.last_name) and getattr(user, 'full_name', None):
            parts = user.full_name.strip().split()
            if parts:
                initial['first_name'] = parts[0]
                initial['last_name'] = ' '.join(parts[1:]) if len(parts) > 1 else ''

        form = UserProfileForm(instance=user, initial=initial)
        
    return render(request, 'edit_profile.html', {
        "form": form,
        "user": user
    })


@login_required
@require_POST
def add_note(request):
    """
    Handles creation of a new note from the dashboard modal.
    """
    form = NoteForm(request.POST)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if form.is_valid():
        note = form.save(commit=False)
        note.user = request.user
        note.save()
        messages.success(request, "Note created successfully!")

        if is_ajax:
            note_data = {
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'subject': note.subject or '',
                'tags': note.tags or '',
                'created_at': note.created_at.strftime('%b %d, %Y'),
                'edit_url': reverse('notes:edit_note', args=[note.id]),
                'delete_url': reverse('notes:delete_note', args=[note.id]),
            }
            total_notes = Note.objects.filter(user=request.user).count()
            return JsonResponse({'status': 'ok', 'note': note_data, 'total_notes': total_notes})
    else:
        # collect form errors to show in messages
        messages.error(request, "Failed to create note. Please check the form.")
        if is_ajax:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    return redirect('notes:home')


@login_required
def edit_note(request, note_id):
    """Edit an existing note for the logged-in user."""
    note = get_object_or_404(Note, id=note_id, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('notes:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NoteForm(instance=note)

    return render(request, 'edit_note.html', {'form': form, 'note': note})


@login_required
def delete_note(request, note_id):
    """Delete a note belonging to the logged-in user."""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('notes:home')
    # If not POST, redirect back
    return redirect('notes:home')

@login_required
def settings_page(request):
    user = request.user
    
    # Initialize form and the flag for opening the modal
    password_form = PasswordChangeForm(user)
    should_open_modal = False # Default to false for GET requests

    if request.method == 'POST':
        # 1. Handle the POST request (password change submission)
        password_form = PasswordChangeForm(user, request.POST)
        
        if password_form.is_valid():
            user = password_form.save()
            
            # Prevents the user from being logged out after password change
            update_session_auth_hash(request, user)  
            
            messages.success(request, 'Your password was successfully updated!')
            
            # Redirect to the GET view to show messages and clear POST data
            return redirect('notes:settings_page')
        else:
            # If the form is invalid, set error message and set flag to reopen modal
            messages.error(request, 'Please correct the error(s) below.')
            should_open_modal = True # Set flag to reopen modal in template
            
    # 2. Calculate the required counts for the statistics blocks
    # NOTE: Using 'status='completed'' based on your profile_view logic
    try:
        total_notes = Note.objects.filter(user=user).count()
        total_tasks = Task.objects.filter(user=user).count()
        completed_tasks_count = Task.objects.filter(user=user, status='completed').count()
    except Exception:
        # Provide safe default values in case models or data access fails
        total_notes = 0
        total_tasks = 0
        completed_tasks_count = 0
    
    # 3. Compile the final context for rendering
    context = {
        'password_form': password_form,
        
        # Pass the calculated stats using the variable names from your template (e.g., {{ total_notes_sidebar }})
        'total_notes_sidebar': total_notes,
        'total_tasks_count': total_tasks,
        'completed_tasks': completed_tasks_count,
        
        # Pass the flag to control modal visibility in JavaScript
        'should_open_modal': should_open_modal,
    }
    
    # 4. Render the template
    return render(request, 'settings_page.html', context)

@login_required
def delete_account(request):
    """
    Handles the permanent deletion of the user's account.
    """
    if request.method == 'POST':
        user = request.user
        
        # 1. Log the user out immediately
        logout(request)
        
        # 2. Delete the user object (and cascade delete related data)
        user.delete()
        
        # 3. Add a success message (will be shown on the homepage/login page)
        messages.success(request, 'Your account was permanently deleted. We are sorry to see you go!')
        
        # 4. Redirect to a non-authenticated page (e.g., login or home)
        # Assuming 'notes:home' is accessible without login, or use a general 'login' page name
        return redirect('notes:home') 
        
    # If a GET request somehow reaches this, redirect them away
    return redirect('notes:settings_page')