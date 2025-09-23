from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import logout

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        from django.contrib.auth import authenticate, login
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successfully!")  # 👈 add here
            return redirect("stunotes:home")  # 👈 redirect to your home
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("stunotes:login")  # back to login if fail

    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "⚠️ User already exists!")
            return redirect("stunotes:register")

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "🎉 Registration successful! Please log in.")
        return redirect("stunotes:login")

    return render(request, "register.html")

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out!")  # 👈 new logout message
    return redirect("stunotes:login")