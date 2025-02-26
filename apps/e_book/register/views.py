# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        context = {
            'username': username,
            'phone': phone,
            'email': email,
        }

        try:
            if not all([username, phone, email, password, confirm_password]):
                messages.error(request, "All fields are required")
                return render(request, 'register/register.html', context)

            if len(username) < 3:
                messages.error(request, "Username must be at least 3 characters long")
                return render(request, 'register/register.html', context)

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return render(request, 'register/register.html', context)

            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "Please enter a valid email address")
                return render(request, 'register/register.html', context)

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return render(request, 'register/register.html', context)

            if not phone.isdigit() or len(phone) < 9:
                messages.error(request, "Please enter a valid phone number (minimum 9 digits)")
                return render(request, 'register/register.html', context)

            if len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long")
                return render(request, 'register/register.html', context)

            if password != confirm_password:
                messages.error(request, "Passwords do not match")
                return render(request, 'register/register.html', context)

            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                messages.success(request, "Registration successful! Please login.")
                return redirect('login')

            except IntegrityError:
                messages.error(request, "An error occurred during registration")
                return render(request, 'register/register.html', context)

        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            return render(request, 'register/register.html', context)

    return render(request, 'register/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        context = {
            'username': username,
        }

        if not all([username, password]):
            messages.error(request, "All fields are required")
            return render(request, 'register/login.html', context)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'register/login.html', context)

    return render(request, 'register/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')
