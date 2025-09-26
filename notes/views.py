from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, logout, authenticate, login

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        username_input = request.POST.get("username")
        email_input = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("notes:register")

        username_field = User.USERNAME_FIELD

        # Determine which field to use for USERNAME_FIELD
        lookup_field = username_input if username_field == "username" else email_input
        if User.objects.filter(**{username_field: lookup_field}).exists():
            messages.error(request, "User already exists!")
            return redirect("notes:register")

        # Create user
        user_kwargs = {username_field: lookup_field, "password": password1}
        user = User.objects.create_user(**user_kwargs)
        if username_field != "username":
            user.username = username_input  # Keep username field if different
            user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect("notes:login")

    return render(request, "register.html")


def login_view(request):
    user_model = get_user_model()  # For template
    if request.method == "POST":
        login_input = request.POST.get("username")  # Works for username or email
        password = request.POST.get("password")

        username_field = User.USERNAME_FIELD
        auth_kwargs = {username_field: login_input, "password": password}

        user = authenticate(request, **auth_kwargs)
        if user:
            login(request, user)
            messages.success(request, "Login successfully!")
            return redirect("notes:home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("notes:login")

    return render(request, "login.html", {"user_model": user_model})


def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out!")
    return redirect("notes:login")
