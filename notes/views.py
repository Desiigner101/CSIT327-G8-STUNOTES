from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout

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
    Render the home page.

    Accessible only to logged-in users.
    """
    return render(request, 'home.html')


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
