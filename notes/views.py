from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Count, Q
from datetime import timedelta
from .models import Task, Note, User, Reminder
from .forms import TaskForm, UserProfileForm, NoteForm, AdminCreationForm, UserCreationForm
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


def landing_view(request):
    """
    Landing page for unauthenticated users. Redirects to `home` if already logged in.
    """
    # If logged-in and not explicitly requesting to show the landing page, redirect to the home dashboard
    if request.user.is_authenticated and not request.GET.get('show_landing'):
        return redirect('notes:home')
    return render(request, 'landing.html')


def login_view(request):
    """
    Handles user login and redirects based on role.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            
            # Redirect based on user role
            # Check if user is admin-only (cannot access user features)
            if hasattr(user, 'is_admin_only') and user.is_admin_only:
                return redirect("notes:admin_dashboard")
            # Check if user is staff/superuser but not admin-only (can switch between views)
            elif user.is_staff or user.is_superuser:
                return redirect("notes:admin_dashboard")
            else:
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
    
    # Check if user is admin-only (cannot access user dashboard)
    if hasattr(user, 'is_admin_only') and user.is_admin_only:
        messages.error(request, "Your account is admin-only and cannot access user features. Please use the Admin Dashboard.")
        return redirect("notes:admin_dashboard")
    
    # Redirect admin users to admin dashboard UNLESS they explicitly want user view
    if (request.user.is_staff or request.user.is_superuser) and not request.session.get('view_as_user', False):
        return redirect("notes:admin_dashboard")
    
    # Rest of the home view code remains the same...
    # Get all user tasks and notes
    tasks = Task.objects.filter(user=user).order_by('-created_at')
    notes = Note.objects.filter(user=user).only('id', 'title', 'subject', 'created_at').order_by('-created_at')[:5]
    
    # Calculate task statistics
    total_tasks = tasks.count()
    completed_tasks_count = tasks.filter(status='completed').count()
    pending_tasks_count = tasks.filter(status='pending').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    
    # Calculate overdue tasks
    now = timezone.now()
    overdue_tasks_count = tasks.filter(
        due_date__lt=now, 
        status__in=['pending', 'in_progress']
    ).count()
    
    # Get today's active tasks
    today = now.date()
    today_tasks = tasks.filter(
        due_date__date=today,
        status__in=['pending', 'in_progress']
    ).order_by('due_date')
    
    # Total notes count
    total_notes = Note.objects.filter(user=user).count()
    
    # Get completed tasks history
    completed_tasks_list = tasks.filter(status='completed').only('id','title','updated_at').order_by('-updated_at')
    
    # Get pending tasks list
    pending_tasks_list = tasks.filter(status='pending').only('id','title','due_date').order_by('due_date')
    
    # Get overdue tasks list
    overdue_tasks_list = tasks.filter(
        due_date__lt=now,
        status__in=['pending', 'in_progress']
    ).only('id','title','due_date').order_by('due_date')
    
    # Get all notes list
    all_notes_list = Note.objects.filter(user=user).only('id','title','subject','created_at').order_by('-created_at')
    
    # Get unique subjects for filter dropdown
    unique_subjects = Note.objects.filter(
        user=user, 
        subject__isnull=False
    ).exclude(
        subject=''
    ).values_list('subject', flat=True).distinct().order_by('subject')

    # Get upcoming tasks due within 24 hours
    next_24h = now + timedelta(hours=24)
    upcoming_tasks = tasks.filter(
        due_date__gte=now,
        due_date__lte=next_24h,
        status__in=['pending', 'in_progress']
    ).only('id','title','due_date').order_by('due_date')
    
    # Detect if editing
    edit_task_id = request.GET.get("edit")
    task_to_edit = None
    edit_form = None

    if edit_task_id:
        task_to_edit = get_object_or_404(Task, id=edit_task_id, user=user)
        edit_form = TaskForm(instance=task_to_edit)

    # Handle POST requests (create or edit task)
    if request.method == "POST":
        if "edit_task_id" in request.POST:
            task_to_edit = get_object_or_404(Task, id=request.POST["edit_task_id"], user=user)
            form = TaskForm(request.POST, instance=task_to_edit)
            if form.is_valid():
                form.save()
                messages.success(request, "Task updated successfully!")
                return redirect("notes:home")
        else:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = user
                task.save()
                messages.success(request, "Task created successfully!")
                return redirect("notes:home")
    else:
        form = TaskForm()

    context = {
        'tasks': tasks.exclude(status='completed')[:10],
        'notes': notes,
        'form': form,
        'edit_form': edit_form,
        'task_to_edit': task_to_edit,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks_count,
        'pending_tasks': pending_tasks_count,
        'in_progress_tasks': in_progress_tasks,
        'overdue_tasks': overdue_tasks_count,
        'total_notes': total_notes,
        'today_tasks': today_tasks,
        'completed_tasks_list': completed_tasks_list,
        'pending_tasks_list': pending_tasks_list,
        'overdue_tasks_list': overdue_tasks_list,
        'all_notes_list': all_notes_list,
        'upcoming_tasks': upcoming_tasks,
        'unique_subjects': unique_subjects,
        'total_tasks_count': total_tasks,
        'total_notes_sidebar': total_notes,
        'view_as_user': request.session.get('view_as_user', False),
    }

    return render(request, "home.html", context)


@login_required
def admin_dashboard(request):
    """
    Admin dashboard with system-wide statistics and management capabilities.
    Only accessible to staff/superuser accounts.
    """
    # Clear the view_as_user flag when accessing admin dashboard
    if 'view_as_user' in request.session:
        del request.session['view_as_user']
    
    # Check if user is admin
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You don't have permission to access the admin dashboard.")
        return redirect("notes:home")
    
    # Get all users
    all_users = User.objects.all()
    total_users = all_users.count()
    admin_users = all_users.filter(Q(is_staff=True) | Q(is_superuser=True)).count()
    regular_users = total_users - admin_users
    
    # Get all tasks and notes
    all_tasks = Task.objects.all()
    all_notes = Note.objects.all()
    
    # Task statistics
    total_tasks = all_tasks.count()
    completed_tasks = all_tasks.filter(status='completed').count()
    pending_tasks = all_tasks.filter(status='pending').count()
    overdue_tasks = all_tasks.filter(
        due_date__lt=timezone.now(),
        status__in=['pending', 'in_progress']
    ).count()
    
    # Note statistics
    total_notes = all_notes.count()
    
    # Recent activity
    recent_users = all_users.order_by('-created_at')[:5]
    recent_tasks = all_tasks.order_by('-created_at')[:10]
    recent_notes = all_notes.order_by('-created_at')[:10]
    
    # User activity statistics
    user_stats = all_users.annotate(
        task_count=Count('tasks'),
        note_count=Count('notes')
    ).order_by('-task_count')[:10]
    
    # Tasks by priority
    high_priority_tasks = all_tasks.filter(priority='high').count()
    medium_priority_tasks = all_tasks.filter(priority='medium').count()
    low_priority_tasks = all_tasks.filter(priority='low').count()
    
    # Get date range for activity chart (last 7 days)
    today = timezone.now().date()
    days_ago_7 = today - timedelta(days=6)
    
    # Activity data for charts
    daily_tasks = []
    daily_notes = []
    date_labels = []
    
    for i in range(7):
        date = days_ago_7 + timedelta(days=i)
        date_labels.append(date.strftime('%b %d'))
        daily_tasks.append(all_tasks.filter(created_at__date=date).count())
        daily_notes.append(all_notes.filter(created_at__date=date).count())
    
    # Determine whether the 'Switch to User View' should be shown in the admin UI
    show_switch_to_user = (not getattr(request.user, 'is_admin_only', False)) and (request.user.is_staff or request.user.is_superuser)

    view_as_user = request.session.get('view_as_user', False)

    # Initialize user form for modal
    user_form = UserCreationForm()
    
    context = {
        # User statistics
        'total_users': total_users,
        'admin_users': admin_users,
        'regular_users': regular_users,
        
        # Task statistics
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'high_priority_tasks': high_priority_tasks,
        'medium_priority_tasks': medium_priority_tasks,
        'low_priority_tasks': low_priority_tasks,
        
        # Note statistics
        'total_notes': total_notes,
        
        # Recent activity
        'recent_users': recent_users,
        'recent_tasks': recent_tasks,
        'recent_notes': recent_notes,
        'user_stats': user_stats,
        'all_users': all_users,  # For delete modal
        
        # Chart data
        'date_labels': date_labels,
        'daily_tasks': daily_tasks,
        'daily_notes': daily_notes,
        
        # Forms
        'user_form': user_form,
        'show_switch_to_user': show_switch_to_user,
        'view_as_user': view_as_user,
    }
    
    return render(request, 'admin_dashboard.html', context)


@login_required
def switch_to_user_mode(request):
    """
    Allow admin to temporarily switch to user view.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You don't have permission to perform this action.")
        return redirect("notes:home")
    
    # Prevent admin-only accounts (admin-only) from switching to user view
    if getattr(request.user, 'is_admin_only', False):
        messages.error(request, "Admin-only accounts cannot access user features.")
        return redirect("notes:admin_dashboard")

    # Set a session flag to indicate admin wants user view
    request.session['view_as_user'] = True
    
    messages.info(request, "Switched to user view. You can return to admin dashboard from settings.")
    return redirect("notes:home")


@login_required
def switch_to_admin_mode(request):
    """
    Clears the 'view_as_user' session flag and takes the user back to the admin dashboard.
    Only available to staff/superusers.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You don't have permission to perform this action.")
        return redirect("notes:home")

    if 'view_as_user' in request.session:
        try:
            del request.session['view_as_user']
        except Exception:
            pass

    messages.info(request, "Returned to Admin mode.")
    return redirect('notes:admin_dashboard')


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
            task.updated_at = timezone.now()
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
    # If request asked for panel rendering (AJAX or panel param), render partial
    panel_mode = request.GET.get('panel') == '1' or request.POST.get('panel') == '1' or request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            if panel_mode:
                return redirect('notes:calendar')
            return redirect('notes:home')
    else:
        form = TaskForm(instance=task)

    if panel_mode:
        return render(request, "includes/edit_task_panel.html", {"form": form, "task": task})

    return render(request, "edit_task.html", {"form": form, "task": task})


@login_required
def profile_view(request):
    """
    Renders the user's profile page and calculates user statistics.
    """
    user = request.user
    # If first/last name are not populated but a full_name exists,
    # derive reasonable first and last name values for display.
    try:
        if (not getattr(user, 'first_name', None) or not getattr(user, 'last_name', None)) and getattr(user, 'full_name', None):
            parts = user.full_name.strip().split()
            if parts:
                # assign non-persisted attributes for template rendering
                user.first_name = parts[0]
                user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
    except Exception:
        # be defensive; if anything goes wrong, fall back to existing attributes
        pass
    
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
        'view_as_user': request.session.get('view_as_user', False),
    }
    return render(request, 'profile_view.html', context)


@login_required
def edit_profile(request):
    """
    Handles displaying and processing the User Profile edit form.
    """
    user = request.user
    # If first/last name are not populated but a full_name exists,
    # derive reasonable first and last name values for display while editing.
    try:
        if (not getattr(user, 'first_name', None) or not getattr(user, 'last_name', None)) and getattr(user, 'full_name', None):
            parts = user.full_name.strip().split()
            if parts:
                # assign non-persisted attributes so templates can read them
                user.first_name = parts[0]
                user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
    except Exception:
        pass
    
    if request.method == "POST":
        # Allow removing current profile picture without changing other fields
        if request.POST.get('remove_profile_pic') == '1':
            try:
                # Delete old file from storage if it's not the default
                old = User.objects.get(pk=user.pk).profile_pic
                if old and getattr(old, 'name', None) and old.name != 'profile_pics/default.jpg':
                    try:
                        old.delete(save=False)
                    except Exception:
                        pass
                # Reset to default image
                user.profile_pic = 'profile_pics/default.jpg'
                user.save(update_fields=['profile_pic'])
                messages.success(request, "Profile picture removed. You can upload a new one.")
            except Exception:
                messages.error(request, "Failed to remove profile picture. Please try again.")
            return redirect("notes:edit_profile")

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            profile = form.save(commit=False)
            if 'profile_pic' in request.FILES:
                try:
                    old = User.objects.get(pk=user.pk).profile_pic
                except User.DoesNotExist:
                    old = None
                if old and getattr(old, 'name', None) and old.name != 'default.jpg':
                    try:
                        old.delete(save=False)
                    except Exception:
                        pass
            profile.first_name = first_name
            profile.last_name = last_name
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
def notes_list(request):
    """Show all notes created by the logged-in user."""
    user = request.user
    notes = Note.objects.filter(user=user).order_by('-created_at')
    total_notes = notes.count()
    context = {
        'notes': notes,
        'total_notes': total_notes,
        'total_tasks_count': Task.objects.filter(user=user).count(),
        'total_notes_sidebar': total_notes,
        'view_as_user': request.session.get('view_as_user', False),
    }
    return render(request, 'notes_list.html', context)


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
    return redirect('notes:home')

@login_required
def settings_page(request):
    user = request.user
    
    password_form = PasswordChangeForm(user)
    admin_form = AdminCreationForm()
    should_open_modal = False
    should_open_admin_modal = False
    should_open_upgrade_modal = False
    should_open_make_user_accessible_modal = False

    if request.method == 'POST':
        # Check if this is a password change request
        if 'old_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('notes:settings_page')
            else:
                messages.error(request, 'Please correct the error(s) below.')
                should_open_modal = True
        
        # Check if this is an upgrade to admin request
        elif 'upgrade_to_admin' in request.POST:
            confirm_password = request.POST.get('confirm_password')
            
            # Verify password
            if user.check_password(confirm_password):
                # Check if user already has tasks/notes (warn them they'll lose access)
                user_tasks = Task.objects.filter(user=user).count()
                user_notes = Note.objects.filter(user=user).count()
                
                # Determine admin-only flag from the form checkbox
                make_admin_only = request.POST.get('make_admin_only') in ['on', '1', 'true', 'True']

                # Upgrade user to admin (optionally admin-only)
                user.is_staff = True
                user.is_superuser = True
                # Mark that this is admin-only account (cannot access user features)
                user.is_admin_only = make_admin_only
                user.save()
                
                messages.success(request, f'Your account has been upgraded to admin! You now have admin-only access.')
                request.session['admin_upgraded'] = {
                    'full_name': user.full_name,
                    'email': user.email,
                    'was_upgrade': True,
                }
                
                return redirect('notes:settings_page')
            else:
                messages.error(request, 'Incorrect password. Please try again.')
                should_open_upgrade_modal = True

        # Check if this is a request to make an admin account user-accessible again
        elif 'make_user_accessible' in request.POST:
            confirm_password = request.POST.get('confirm_password_user_access')
            if user.check_password(confirm_password):
                user.is_admin_only = False
                user.save()
                messages.success(request, 'Your account now has user access in addition to admin.')
                return redirect('notes:settings_page')
            else:
                messages.error(request, 'Incorrect password. Please try again.')
                # Open the 'make user accessible' modal back up with error
                should_open_make_user_accessible_modal = True
        
        # Check if this is a create new admin request
        elif 'create_admin' in request.POST:
            admin_form = AdminCreationForm(request.POST)
            
            if admin_form.is_valid():
                full_name = admin_form.cleaned_data['full_name']
                email = admin_form.cleaned_data['email']
                password = admin_form.cleaned_data['password1']
                is_admin_only_flag = admin_form.cleaned_data.get('is_admin_only', False)
                
                # Check if user with this email already exists
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'An account with this email already exists. Use "Upgrade to Admin" to upgrade an existing account, or choose a different email.')
                    should_open_admin_modal = True
                else:
                    # Create new admin-only user
                    admin_user = User.objects.create_user(
                        email=email,
                        username=email,
                        full_name=full_name,
                        password=password,
                        is_staff=True,
                        is_superuser=True,
                        is_admin_only=is_admin_only_flag  # Honor the admin-only flag
                    )
                    
                    messages.success(request, f'Admin account created successfully for {admin_user.full_name}!')
                    request.session['admin_upgraded'] = {
                        'full_name': admin_user.full_name,
                        'email': admin_user.email,
                        'was_upgrade': False,
                    }
                    
                    return redirect('notes:settings_page')
            else:
                messages.error(request, 'Please correct the errors below.')
                should_open_admin_modal = True
            
    try:
        total_notes = Note.objects.filter(user=user).count()
        total_tasks = Task.objects.filter(user=user).count()
        completed_tasks_count = Task.objects.filter(user=user, status='completed').count()
    except Exception:
        total_notes = 0
        total_tasks = 0
        completed_tasks_count = 0
    
    # Check if admin was just created/upgraded (to show success modal)
    admin_upgraded_info = None
    should_show_admin_success = False
    if 'admin_upgraded' in request.session:
        admin_upgraded_info = request.session.pop('admin_upgraded')
        should_show_admin_success = True
    
    # Check if user is viewing as regular user (for sidebar navigation)
    view_as_user = request.session.get('view_as_user', False)
    
    context = {
        'password_form': password_form,
        'admin_form': admin_form,
        'total_notes_sidebar': total_notes,
        'total_tasks_count': total_tasks,
        'completed_tasks': completed_tasks_count,
        'should_open_modal': should_open_modal,
        'should_open_admin_modal': should_open_admin_modal,
        'should_open_upgrade_modal': should_open_upgrade_modal,
        'should_open_make_user_accessible_modal': should_open_make_user_accessible_modal,
        'is_admin': user.is_staff or user.is_superuser,
        'view_as_user': view_as_user,
        'admin_upgraded_info': admin_upgraded_info,
        'should_show_admin_success': should_show_admin_success,
    }
    
    return render(request, 'settings_page.html', context)


@login_required
def calendar_view(request):
    """
    Displays a month calendar with tasks' due dates and reminders.
    """
    user = request.user
    # Gather tasks with due dates and reminders, but exclude tasks that are completed
    tasks_with_due = Task.objects.filter(user=user, due_date__isnull=False).exclude(status='completed').order_by('due_date')
    # Exclude reminders that belong to completed tasks
    reminders = Reminder.objects.filter(task__user=user).exclude(task__status='completed').order_by('remind_time')

    # Build combined upcoming events list
    upcoming = []
    for t in tasks_with_due:
        upcoming.append({
            'type': 'task',
            'title': t.title,
            'datetime': t.due_date,
            'url': reverse('notes:edit_task', args=[t.id])
        })
    for r in reminders:
        upcoming.append({
            'type': 'reminder',
            'title': f"Reminder: {r.task.title}",
            'datetime': r.remind_time,
            'url': reverse('notes:edit_task', args=[r.task.id])
        })

    # Sort by datetime
    upcoming_sorted = sorted(upcoming, key=lambda e: e['datetime'] or timezone.now())

    # Generate month grid for current month
    import calendar as _pycal
    now = timezone.localtime(timezone.now())
    year = now.year
    month = now.month
    cal = _pycal.Calendar()
    month_weeks = cal.monthdayscalendar(year, month)

    # Map day -> events
    events_by_day = {}
    for ev in upcoming_sorted:
        dt = timezone.localtime(ev['datetime']) if ev['datetime'] else None
        if dt and dt.year == year and dt.month == month:
            events_by_day.setdefault(dt.day, []).append(ev)

    # Build a structure where each week is a list of day dicts {day: int, events: []}
    month_cells = []
    for week in month_weeks:
        week_cells = []
        for day in week:
            if day == 0:
                week_cells.append({'day': 0, 'events': []})
            else:
                week_cells.append({'day': day, 'events': events_by_day.get(day, [])})
        month_cells.append(week_cells)

    context = {
        'month_cells': month_cells,
        'year': year,
        'month': now.strftime('%B'),
        'upcoming': upcoming_sorted[:30],
        # Prepare todos for today and tomorrow
        'todos_today': [e for e in upcoming_sorted if (timezone.localtime(e['datetime']).date() == now.date())],
        'todos_tomorrow': [e for e in upcoming_sorted if (timezone.localtime(e['datetime']).date() == (now + timedelta(days=1)).date())],
        'total_tasks_count': Task.objects.filter(user=user).count(),
        'total_notes_sidebar': Note.objects.filter(user=user).count(),
        'view_as_user': request.session.get('view_as_user', False),
    }

    # expose 'now' for template use
    context['now'] = now

    return render(request, 'calendar.html', context)

@login_required
def delete_account(request):
    """
    Handles the permanent deletion of the user's account.
    """
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account was permanently deleted. We are sorry to see you go!')
        return redirect('notes:home') 
        
    return redirect('notes:settings_page')


@login_required
@require_POST
def add_user(request):
    """
    Allows admin to create a new regular user account.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You don't have permission to add users.")
        return redirect("notes:admin_dashboard")
    
    form = UserCreationForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        full_name = form.cleaned_data['full_name']
        password = form.cleaned_data['password1']
        
        # Create the user
        user = User.objects.create_user(
            email=email,
            username=email,
            full_name=full_name,
            password=password
        )
        
        messages.success(request, f'User "{full_name}" has been successfully created!')
    else:
        # If form is invalid, show errors
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')
    
    return redirect('notes:admin_dashboard')


@login_required
@require_POST
def delete_user(request, user_id):
    """
    Allows admin to delete a user account.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You don't have permission to delete users.")
        return redirect("notes:admin_dashboard")
    
    try:
        user_to_delete = get_object_or_404(User, id=user_id)
        
        # Prevent admin from deleting themselves
        if user_to_delete.id == request.user.id:
            messages.error(request, "You cannot delete your own account.")
            return redirect('notes:admin_dashboard')
        
        # Prevent deleting superusers (optional safety check)
        if user_to_delete.is_superuser and not request.user.is_superuser:
            messages.error(request, "You don't have permission to delete superuser accounts.")
            return redirect('notes:admin_dashboard')
        
        user_name = user_to_delete.full_name or user_to_delete.email
        user_to_delete.delete()
        messages.success(request, f'User "{user_name}" has been successfully deleted.')
        
    except Exception as e:
        messages.error(request, f'Error deleting user: {str(e)}')
    
    return redirect('notes:admin_dashboard')