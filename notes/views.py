from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task, Note
from .forms import TaskForm, UserProfileForm

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
    
    # ✅ Get today's tasks
    today = now.date()
    today_tasks = tasks.filter(due_date__date=today).order_by('due_date')
    
    # ✅ Total notes count
    total_notes = Note.objects.filter(user=user).count()
    
    # ✅ Get completed tasks history
    completed_tasks_list = tasks.filter(status='completed').order_by('-updated_at')
    
    # ✅ NEW: Get pending tasks list
    pending_tasks_list = tasks.filter(status='pending').order_by('due_date')
    
    # ✅ NEW: Get overdue tasks list
    overdue_tasks_list = tasks.filter(
        due_date__lt=now,
        status__in=['pending', 'in_progress']
    ).order_by('due_date')
    
    # ✅ NEW: Get all notes list
    all_notes_list = Note.objects.filter(user=user).order_by('-created_at')
    
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
        'pending_tasks_list': pending_tasks_list,       # ✅ NEW
        'overdue_tasks_list': overdue_tasks_list,       # ✅ NEW
        'all_notes_list': all_notes_list,               # ✅ NEW
        
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
        form = UserProfileForm(request.POST, request.FILES, instance=user) 
        
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("notes:profile_view")
        else:
            messages.error(request, "Please correct the errors below.")
            
    else:
        form = UserProfileForm(instance=user)
        
    return render(request, 'edit_profile.html', {
        "form": form,
        "user": user
    })