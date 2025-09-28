from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from .models import Task, Note
from .forms import TaskForm, UserProfileForm



# Get the custom User model
User = get_user_model()

def register_view(request):
    """
    Handles user registration.

    Methods:
    - GET: Render the registration form.
    - POST: Process registration data.

    Steps on POST:
    1. Retrieve full_name, email, password1, and password2 from the form.
    2. Validate that both passwords match. Show error if they don't.
    3. Check if a user with the provided email already exists. Show error if yes.
    4. Create a new User instance with the provided details.
    5. Show a success message and redirect to login page.
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
            username=email,  # username still required by AbstractUser
            full_name=full_name,
            password=password1
        )

        messages.success(request, "Registration successful! Please log in.")
        return redirect("notes:login")

    # Render registration form for GET requests
    return render(request, "register.html")


def login_view(request):
    """
    Handles user login.

    Methods:
    - GET: Render the login form.
    - POST: Authenticate user credentials.

    Steps on POST:
    1. Retrieve email and password from the form.
    2. Authenticate user using email and password.
    3. If authentication succeeds, log in the user and redirect to home.
    4. If authentication fails, display an error and redirect to login page.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)  # Log in the user
            messages.success(request, "Login successful!")
            return redirect("notes:home")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("notes:login")

    # Render login form for GET requests
    return render(request, "login.html")

def home(request):
    """
    Render the home page with tasks and task form.
    Now handles both authenticated and anonymous users.
    """
    # Check if user is authenticated before filtering tasks
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    else:
        tasks = []  # Empty list for anonymous users
        # You might want to redirect to login instead:
        # return redirect("notes:login")

    # detect if editing (only for authenticated users)
    edit_task_id = request.GET.get("edit")
    task_to_edit = None
    edit_form = None

    if edit_task_id and request.user.is_authenticated:
        task_to_edit = get_object_or_404(Task, id=edit_task_id, user=request.user)
        edit_form = TaskForm(instance=task_to_edit)

    if request.method == "POST":
        # Only allow POST operations for authenticated users
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to perform this action.")
            return redirect("notes:login")
            
        if "edit_task_id" in request.POST:  # ✅ Editing
            task_to_edit = get_object_or_404(Task, id=request.POST["edit_task_id"], user=request.user)
            form = TaskForm(request.POST, instance=task_to_edit)
            if form.is_valid():
                form.save()
                return redirect("notes:home")
        else:  # ✅ Adding new
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return redirect("notes:home")
    else:
        form = TaskForm()

    return render(request, "home.html", {
        "tasks": tasks,
        "form": form,
        "edit_form": edit_form,
        "task_to_edit": task_to_edit,
    })

def logout_view(request):
    """
    Logs out the current user and redirects to login page.

    Steps:
    1. Call Django's logout() to end the session.
    2. Display a logout success message.
    3. Redirect user to the login page.
    """
    logout(request)
    messages.success(request, "You have logged out!")
    return redirect("notes:login")

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('notes:home')
    return redirect('notes:home')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('notes:home')
    else:
        form = TaskForm(instance=task)

    return render(request, "edit_task.html", {"form": form, "task": task})

 # Added security decorator
def profile_view(request):
    """
    Renders the user's profile page and calculates user statistics.
    """
    user = request.user
    
    # 1. Calculate Task Statistics
    total_tasks = Task.objects.filter(user=user).count()
    completed_tasks = Task.objects.filter(user=user, status='completed').count()
    
    # 2. Calculate Note Statistics
    total_notes = Note.objects.filter(user=user).count() # <--- CRITICAL FIX 2: Changed 'notes' to 'Note'
    
    context = {
        'user': user,
        'total_notes_created': total_notes,
        'total_tasks_created': total_tasks, # Display total tasks created
        'tasks_completed': completed_tasks, # Display tasks completed
    }
    return render(request, 'profile_view.html', context)

def edit_profile(request):
    """
    Handles displaying and processing the User Profile edit form, including file upload.
    """
    user = request.user
    
    if request.method == "POST":
        # CRITICAL: Pass request.FILES to the form for file handling
        form = UserProfileForm(request.POST, request.FILES, instance=user) 
        
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile and picture have been updated successfully!")
            return redirect("notes:profile_view")
        else:
            messages.error(request, "Please correct the errors below.")
            
    else:
        form = UserProfileForm(instance=user)
        
    return render(request, 'edit_profile.html', {
        "form": form,
        "user": user
    })