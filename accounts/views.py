from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm
from .models import UserProfile


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('prediction:home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('prediction:home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def signup_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('prediction:home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile
            UserProfile.objects.create(user=user)
            # Auto-login after signup
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.first_name or user.username}!')
            return redirect('prediction:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')
